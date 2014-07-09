# coding=utf-8

from os import wait
from signal import signal, SIGINT, SIG_IGN
from socket import AF_INET, SOL_SOCKET, SO_REUSEADDR

from gevent.socket import socket
from gevent.pywsgi import WSGIServer
from gevent.os import fork
from gevent.threadpool import ThreadPool
from gevent.event import Event

from engine.config import HOST, PORT, WORKERS, CPUS


class Application(object):

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)

    def run(self):
        # 监听
        sock = socket(family=AF_INET)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1024)
        sock.setblocking(0)

        # 创建子进程
        childs = []
        for i in range(WORKERS or CPUS * 2 + 1):
            pid = fork()

            if pid > 0:
                childs.append(pid)
            else:
                self._child(sock)

        # 父进程，等待所有子进程退出。
        self._parent(childs)

    def _parent(self, childs):
        signal(SIGINT, SIG_IGN)

        while childs:
            pid, _ = wait()
            childs.remove(pid)

    def _child(self, sock):
        signal(SIGINT, lambda *args: exit(0))

        server = WSGIServer(sock, self._execute, spawn="default", log=None)
        server.serve_forever()

    def _execute(self, environ, start_response):
        handler, kwargs = self._server.match(environ)
        args = (environ, start_response, handler, kwargs)

        if hasattr(handler, "__async__"):
            e = Event()
            g = self._pool.apply_async(self._server.execute, args, callback=lambda ret: e.set())
            e.wait()
            return g.get()

        return self._server.execute(*args)
