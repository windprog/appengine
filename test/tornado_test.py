#!/usr/bin/env python
# coding=utf-8

import time
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.gen

# import futures
# pool = futures.ThreadPoolExecutor(8)


def test():
    time.sleep(0.01)
    return "Hello, World!\n"


# class HelloAsyncHandler(tornado.web.RequestHandler):

#     @tornado.web.asynchronous
#     @tornado.gen.coroutine
#     def get(self):
#         s = yield pool.submit(test)
#         self.write(s)


class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(test())


application = tornado.web.Application([
    # (r"/", HelloAsyncHandler),
    (r"/", HelloHandler),
])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(9)  # Forks multiple sub-processes
    tornado.ioloop.IOLoop.instance().start()
