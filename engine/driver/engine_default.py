# coding=utf-8

from __future__ import print_function

from os import wait, WIFEXITED
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
from engine.decorator import TAG_ASYNC
from engine.util import app_path


class Engine(BaseEngine, Signaler):

    #
    # * 基于 gevent.pywsgi 实现。
    # * 支持多 worker 进程。
    # * 支持 thread pool 异步执行。
    #

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)
        self._pids = []
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

        self._fork(WORKERS or CPUS * 2 + 1)
        self._parent()

    # --- parent ---------------------------------------------------------------- #

    def _fork(self, num):
        for i in range(num):
            pid = fork()

            if pid > 0:
                self._pids.append(pid)
            else:
                self._worker()
                exit(0)

    def _parent(self):
        # 注册信号。
        self.parent_signal(self._fork)

        # 等待所有子进程退出。
        while self._pids:
            try:
                pid, status = wait()

                # 如果子进程非正常退出，新建。
                (not WIFEXITED(status)) and self._fork(1)
            except OSError:
                continue

            self._pids.remove(pid)

    # --- worker ---------------------------------------------------------------- #

    def _worker(self):
        # 注册信号。
        self.worker_signal(self._stop)

        # 启动服务器。
        kwargs = HTTPS and \
            {k: app_path("ssl/" + v) for k, v in (("keyfile", HTTPS_KEY), ("certfile", HTTPS_CERT))} or \
            {}

        self._wsgi_server = WSGIServer(self._listen_sock, self._handler, log=None, **kwargs)
        self._wsgi_server.serve_forever()

        # 等待所有处理结束，超时 10 秒。
        hasattr(self._wsgi_server, "__graceful__") and gwait(timeout=10)

    def _stop(self, graceful=True):
        # 停止服务器。
        stop = lambda *args: self._wsgi_server and self._wsgi_server.stop()
        graceful and (setattr(self._wsgi_server, "__graceful__", True), stop()) or stop()

    def _handler(self, environ, start_response):
        # 请求处理。
        handler, kwargs = self._server.match(environ)
        args = (environ, start_response, handler, kwargs)

        if hasattr(handler, TAG_ASYNC):
            e = Event()
            g = self._pool.apply_async(self._server.execute, args, callback=lambda ret: e.set())
            e.wait()
            return g.get()

        return self._server.execute(*args)
