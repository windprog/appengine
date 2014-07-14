# coding=utf-8

from config import DEBUG, Engine
from router import Router
from parser import Request, Response
from debug import DebugEngine
from decorator import TAG_ASYNC
from helper import not_found

#
# TODO
# ~~~~~~~~~
#


class Server(object):

    def __init__(self):
        self._engine = DEBUG and DebugEngine(self) or Engine(self)

    def run(self):
        self._engine.run()

    def execute(self, environ, start_response):
        # 匹配 URL 路由，返回 (handler, kwargs)。
        handler, kwargs = Router.instance.match(environ)

        if handler is None:
            return not_found(start_response)

        # 根据 Handler 参数列表动态构建实参对象。
        # 省略掉不需要的中间对象，以提升性能，减少 GC 压力。
        handler_args = handler.func_code.co_varnames[:handler.func_code.co_argcount]

        if "environ" in handler_args:
            kwargs["environ"] = environ
        if "start_response" in handler_args:
            kwargs["start_response"] = start_response
        if "request" in handler_args:
            kwargs["request"] = Request(environ)
        if "response" in handler_args:
            kwargs["response"] = Response()

        # 执行。
        ret = hasattr(handler, TAG_ASYNC) and self._engine.async_execute(handler, **kwargs) or handler(**kwargs)

        # 处理结果。
        if "response" in handler_args:
            return kwargs["response"](environ, start_response)
        elif not "start_response" in handler_args:
            return Response(ret)(environ, start_response)
        elif hasattr(ret, "__iter__"):
            return ret

        return (ret,)
