# coding=utf-8

from util import walk_members
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


class Router(object):

    # ---- 描述符: 延迟实例化。------------------------ #

    class InstanceDescriptor(object):

        def __get__(self, instance, owner):
            v = getattr(owner, "__instance__", None)
            if not v:
                v = owner()  # 构造参数!
                owner.__instance__ = v

            return v

    # ----------------------------------------------- #

    def __init__(self):
        self._handlers = {}
        self._selector = Selector()
        self.load()

    handlers = property(lambda self: self._handlers)
    instance = InstanceDescriptor()

    def load(self):
        # 通过检查 __urls__，载入所有 handler。

        def add(url, handler):
            self._selector.add(url, handler)
            self._handlers[url] = handler

        walk_members(Action,
                     lambda m: hasattr(m, "__urls__"),
                     lambda h: map(lambda (k, v): add(k, v), ((u, h) for u in h.__urls__)))

    def reset(self):
        # 重置(清空) Handlers 配置。
        self._selector.reset()
        return self

    def match(self, environ):
        # 返回 handler 和 kwargs。
        return self._selector.match(environ)
