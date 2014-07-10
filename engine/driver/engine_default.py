# coding=utf-8

from __future__ import print_function

from os import wait
from socket import AF_INET, SOL_SOCKET, SO_REUSEADDR

from gevent import wait as gwait
from gevent.socket import socket
from gevent.pywsgi import WSGIServer
from gevent.os import fork
from gevent.threadpool import ThreadPool
from gevent.event import Event

from engine.config import HOST, PORT, WORKERS, CPUS, HTTPS, HTTPS_KEY, HTTPS_CERT
from engine.signaler import Signaler
from engine.interface import BaseApplication
from engine.util import app_path


class Application(BaseApplication, Signaler):

    #
    # * 基于 gevent.pywsgi 实现。
    # * 支持多 worker 进程。
    # * 支持 thread pool 异步执行。
    #

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)
        self._childs = []
        self._wsgi_server = None

        BaseApplication.__init__(self, server)
        Signaler.__init__(self)

    def run(self):
        # 监听
        sock = socket(family=AF_INET)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(2048)
        sock.setblocking(0)

        # 创建子进程
        for i in range(WORKERS or CPUS * 2 + 1):
            pid = fork()

            if pid > 0:
                self._childs.append(pid)
            else:
                # 子进程。
                self._child_execute(sock)
                exit(0)

        # 父进程。
        self._parent_execute()

    def _parent_execute(self):
        self.parent_signal()

        # 等待所有子进程退出。
        while self._childs:
            try:
                pid, _ = wait()
            except OSError:
                continue

            self._childs.remove(pid)

    def _child_execute(self, sock):
        def singal():
            # 信号处理。
            stop = lambda *args: self._wsgi_server and self._wsgi_server.stop()
            self.child_signal(
                lambda *args: stop(),  # Quick shutdown
                lambda *args: (setattr(self._wsgi_server, "__graceful__", True), stop())  # Graceful shutdown
            )

        def server():
            # HTTPS 参数。
            kwargs = HTTPS and \
                {k: app_path("ssl/" + v) for k, v in (("keyfile", HTTPS_KEY), ("certfile", HTTPS_CERT))} or \
                {}

            # 启动 WSGI-Server。
            self._wsgi_server = WSGIServer(sock, self._handler, spawn="default", log=None, **kwargs)
            self._wsgi_server.serve_forever()

            # 等待所有处理结束，超时 10 秒。
            hasattr(self._wsgi_server, "__graceful__") and gwait(timeout=10)

        singal()
        server()

    def _handler(self, environ, start_response):
        handler, kwargs = self._server.match(environ)
        args = (environ, start_response, handler, kwargs)

        if hasattr(handler, "__async__"):
            e = Event()
            g = self._pool.apply_async(self._server.execute, args, callback=lambda ret: e.set())
            e.wait()
            return g.get()

        return self._server.execute(*args)
