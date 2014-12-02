# coding=utf-8

from abc import ABCMeta, abstractmethod

#
# 各驱动调用接口规范。
#


class BaseEngine(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, server):
        pass

    @abstractmethod
    def async_execute(self, func, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass


class BaseSelector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add(self, url, methods, handler):
        pass

    @abstractmethod
    def reset(self):
        # 重置路由表。
        pass

    @abstractmethod
    def match(self, environ):
        # 返回 (handler, kwargs)。
        pass


class BaseRequest(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, environ):
        pass


class BaseResponse(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, environ, start_response):
        # 转换成 WSGI 调用。
        pass

    @abstractmethod
    def set_data(self, data):
        # 设置输出数据。
        pass
