# coding=utf-8

# 默认路由选择器

from werkzeug.routing import Map, Rule


class Selector(object):

    def __init__(self):
        super(Selector, self).__init__()
        self.maps = Map()

    def add(self, url, handler):
        self.maps.add(Rule(url, endpoint=handler))

    def match(self, environ):
        # 返回 (handler, kwargs)。
        urls = self.maps.bind_to_environ(environ)
        return urls.match()
