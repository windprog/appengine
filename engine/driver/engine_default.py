# coding=utf-8

from gevent.event import Event
from gevent.threadpool import ThreadPool
from gunicorn.app.base import BaseApplication

from engine.config import HOST, PORT, WORKERS, CPUS


class Application(BaseApplication):

    def __init__(self, server):
        self._server = server
        self._pool = ThreadPool(CPUS * 4)
        super(Application, self).__init__()

    def load_config(self):
        options = {
            "bind": "{0}:{1}".format(HOST, PORT),
            "workers": WORKERS or CPUS * 2 + 1,
            "worker_class": "gevent",
        }

        map(lambda (k, v): self.cfg.set(k, v), options.items())

    def load(self):
        return self._execute

    def _execute(self, environ, start_response):
        # 调用 Server.match 匹配合适的 Handler。
        # 检查异步标记来决定执行方式，具体调用由 Server.execute 完成。

        handler, kwargs = self._server.match(environ)
        args = (environ, start_response, handler, kwargs)

        if hasattr(handler, "__async__"):
            e = Event()
            g = self._pool.apply_async(self._server.execute, args, callback=lambda ret: e.set())
            e.wait()
            return g.get()

        return self._server.execute(*args)
