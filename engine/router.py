# coding=utf-8

from util import walk_members
from config import Selector, Action
from decorator import TAG_URLS


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
        self._handlers = {}  # {url:(handler, methods)}
        self._selector = Selector()
        self.load()

    handlers = property(lambda self: self._handlers)
    instance = InstanceDescriptor()

    def load(self):
        # 通过检查 urls 标记，载入所有 handler。

        def add(handler):
            for url, methods in getattr(handler, TAG_URLS).iteritems():
                self._selector.add(url, methods, handler)
                self._handlers[url] = (handler, methods)

        walk_members(Action, lambda m: hasattr(m, TAG_URLS), add)

    def reset(self):
        # 重置(清空) Handlers 配置。
        self._selector.reset()
        return self

    def match(self, environ):
        # 返回 handler 和 kwargs。
        return self._selector.match(environ)
