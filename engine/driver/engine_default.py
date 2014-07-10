# coding=utf-8

from os import wait
from signal import SIGINT, SIG_IGN
from socket import AF_INET, SOL_SOCKET, SO_REUSEADDR

from gevent import signal, wait as gwait
from gevent.socket import socket
from gevent.pywsgi import WSGIServer
from gevent.os import fork
from gevent.threadpool import ThreadPool
from gevent.event import Event

from engine.config import HOST, PORT, WORKERS, CPUS
from engine.interface import BaseApplication


class Application(BaseApplication):

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)
        self._childs = []
        self._wsgi_server = None

    def run(self):
        # 监听
        sock = socket(family=AF_INET)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1024)
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
        signal(SIGINT, SIG_IGN)

        # 等待所有子进程退出。
        while self._childs:
            pid, _ = wait()
            self._childs.remove(pid)

    def _child_execute(self, sock):
        # 信号处理:
        # * INT: 停止服务，结束子进程。
        signal(SIGINT, lambda *args: self._wsgi_server and self._wsgi_server.stop())

        # 启动 WSGI-Server。
        self._wsgi_server = WSGIServer(sock, self._handler, spawn="default", log=None)
        self._wsgi_server.serve_forever()

        # 等待所有处理结束，超时 10 秒。
        gwait(timeout=10)

    def _handler(self, environ, start_response):
        handler, kwargs = self._server.match(environ)
        args = (environ, start_response, handler, kwargs)

        if hasattr(handler, "__async__"):
            e = Event()
            g = self._pool.apply_async(self._server.execute, args, callback=lambda ret: e.set())
            e.wait()
            return g.get()

        return self._server.execute(*args)
