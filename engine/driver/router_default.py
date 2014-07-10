# coding=utf-8

from werkzeug.routing import Map, Rule
from engine.interface import BaseSelector


class Selector(BaseSelector):

    def __init__(self):
        self.reset()

    def add(self, url, handler):
        self._maps.add(Rule(url, endpoint=handler))

    def reset(self):
        self._maps = Map()

    def match(self, environ):
        # 返回 (handler, kwargs)。
        urls = self._maps.bind_to_environ(environ)
        return urls.match()
