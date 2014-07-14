# coding=utf-8

from __future__ import print_function
from socket import AF_INET, SOL_SOCKET, SO_REUSEADDR

from gevent import wait as gwait
from gevent.socket import socket
from gevent.pywsgi import WSGIServer
from gevent.os import fork
from gevent.threadpool import ThreadPool
from gevent.event import Event

from engine.config import HOST, PORT, WORKERS, CPUS, HTTPS, HTTPS_KEY, HTTPS_CERT
from engine.signaler import Signaler
from engine.interface import BaseEngine
from engine.util import app_path


# from gevent.monkey import patch_all
# patch_all()


class Engine(BaseEngine, Signaler):

    #
    # * 基于 gevent.pywsgi 实现。
    # * 支持多 worker 进程。
    # * 支持 thread pool 异步执行。
    #

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)
        self._listen_sock = None
        self._wsgi_server = None

        BaseEngine.__init__(self, server)
        Signaler.__init__(self)

    def run(self):
        self._listen_sock = socket(family=AF_INET)
        self._listen_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._listen_sock.bind((HOST, PORT))
        self._listen_sock.listen(2048)
        self._listen_sock.setblocking(0)

        self.fork_workers(WORKERS or CPUS)
        self.parent_execute()

    def fork_workers(self, num):
        for i in range(num):
            if fork() == 0:
                self.worker_execute()
                exit(0)

    def worker_execute(self):
        Signaler.worker_execute(self)

        # 启动服务器。
        kwargs = HTTPS and \
            {k: app_path("ssl/" + v) for k, v in (("keyfile", HTTPS_KEY), ("certfile", HTTPS_CERT))} or \
            {}

        self._wsgi_server = WSGIServer(self._listen_sock, self._server.execute, log=None, **kwargs)
        self._wsgi_server.serve_forever()

        # 等待所有处理结束，超时 10 秒。
        hasattr(self._wsgi_server, "__graceful__") and gwait(timeout=10)

    def worker_stop(self, graceful):
        stop = lambda *args: self._wsgi_server and self._wsgi_server.stop()
        graceful and (setattr(self._wsgi_server, "__graceful__", True), stop()) or stop()

    def async_execute(self, func, *args, **kwargs):
        e = Event()
        g = self._pool.apply_async(func, args, kwargs, callback=lambda ret: e.set())
        e.wait()
        return g.get()
