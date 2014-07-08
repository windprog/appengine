# coding=utf-8

# 默认路由选择器

from werkzeug.routing import Map, Rule


class Selector(object):

    def __init__(self):
        super(Selector, self).__init__()
        self.reset()

    def add(self, url, handler):
        self._maps.add(Rule(url, endpoint=handler))

    def reset(self):
        self._maps = Map()

    def match(self, environ):
        # 返回 (handler, kwargs)。
        urls = self._maps.bind_to_environ(environ)
        return urls.match()
