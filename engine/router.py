# coding=utf-8

from util import singleton, walk_members
from config import Selector, Action

#
#  Selector Driver Interface
#  -----------------------------------------------------------
#  class Selector:
#      def __init__(self): pass
#      def add(self, url, handler): pass
#      def reset(self): pass
#      def match(self, environ): pass  --> (handler, kwargs)
#


@singleton
class Router(object):

    def __init__(self):
        self._selector = Selector()
        self.load()

    def load(self):
        # 通过检查 __urls__，载入所有 handler。
        walk_members(Action,
                     lambda m: hasattr(m, "__urls__"),
                     lambda h: map(lambda (u, h): self._selector.add(u, h), ((u, h) for u in h.__urls__)))

    def reset(self):
        # 重置(清空) Handlers 配置。
        self._selector.reset()
        return self

    def match(self, environ):
        # 返回 handler 和 kwargs。
        return self._selector.match(environ)


def url(*paths):
    # 添加 __urls__ 标记。
    def set(cls):
        if not hasattr(cls, "__urls__"):
            cls.__urls__ = []

        cls.__urls__.extend(paths)
        return cls

    return set
