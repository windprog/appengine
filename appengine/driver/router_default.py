# coding=utf-8

from werkzeug.routing import Map, Rule
from ..interface import BaseSelector


class Selector(BaseSelector):

    #
    # 基于 werkzeug (flask 项目) 实现。
    # 未来会被自主实现替换。
    #

    def __init__(self):
        self.reset()

    def add(self, url, methods, handler):
        self._maps.add(Rule(url, methods=methods, endpoint=handler))

    def reset(self):
        self._maps = Map()

    def match(self, environ):
        # 返回 (handler, kwargs)。
        try:
            urls = self._maps.bind_to_environ(environ)
            return urls.match()
        except:
            return None, None
