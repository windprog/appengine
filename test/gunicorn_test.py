#!/usr/bin/env python
# coding=utf-8

import time
osleep = time.sleep  # gevent.patch_sleep

import multiprocessing

import gevent
import gevent.event
import gevent.threadpool
import gunicorn.app.base

cpus = multiprocessing.cpu_count()
pool = gevent.threadpool.ThreadPool(cpus * 4)


def test():
    osleep(0.01)
    return "Hello, World!\n"


def handler(environ, start_response):
    e = gevent.event.Event()
    g = pool.apply_async(test, callback=lambda ret: e.set())
    e.wait()
    s = g.get()

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    yield s


class Application(gunicorn.app.base.BaseApplication):

    def __init__(self):
        super(Application, self).__init__()

    def load_config(self):
        options = {
            "bind": ["0.0.0.0:8888"],
            "workers": cpus * 2 + 1,
            "worker_class": "gevent",
            # "loglevel": "error",
            # "accesslog": "-",
            # "errorlog": "-",
        }

        map(lambda (k, v): self.cfg.set(k, v), options.items())

    def load(self):
        return handler


if __name__ == "__main__":
    Application().run()
