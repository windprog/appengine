# coding=utf-8

from .util import walk_members
from .config import settings
from ..decorator import TAG_URLS, TAG_FUNC


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
        self._selector = settings.Selector()
        self._cache = {}
        self.load()

    handlers = property(lambda self: self._handlers)
    instance = InstanceDescriptor()

    def load(self):
        # 通过检查 urls 标记，载入所有 handler。

        def add(handler):
            for url, methods in getattr(handler, TAG_URLS).iteritems():
                self._selector.add(url, methods, handler)
                # 让程序开始运行时输出正确信息
                if hasattr(handler, TAG_FUNC):
                    handler = getattr(handler, TAG_FUNC)
                self._handlers[url] = (handler, methods)

        for mod in settings.Action_module_list:
            walk_members(mod, lambda m: hasattr(m, TAG_URLS), add)

    def reset(self):
        # 重置(清空) Handlers 配置。
        self._selector.reset()
        return self

    def match(self, environ):
        # 从缓存中查找固定 URL 匹配。
        key = "{0}|{1}".format(environ["REQUEST_METHOD"], environ["PATH_INFO"])
        handler = self._cache.get(key, None)
        if not settings.DEBUG and handler:
            return handler, {}

        handler, kwargs = self._selector.match(environ)

        # 如果 URL 固定，没有分解参数，缓存。
        if not kwargs and key not in self._cache:
            self._cache[key] = handler

        return handler, kwargs
