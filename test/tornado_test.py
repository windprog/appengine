#!/usr/bin/env python
# coding=utf-8

import time

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.gen


class AsyncHandler(tornado.web.RequestHandler):

    def test(self, callback):
        time.sleep(0.01)
        callback("Hello, World!\n")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        s = yield tornado.gen.Task(self.test)
        self.write(s)


class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, World!\n")


application = tornado.web.Application([
    (r"/async", AsyncHandler),
    (r"/", HelloHandler),
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)  # Forks multiple sub-processes
    tornado.ioloop.IOLoop.instance().start()
