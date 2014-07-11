# coding=utf-8

from config import DEBUG, Engine
from router import Router
from parser import Request, Response
from debug import DebugEngine
from helper import not_found

#
# TODO:
# ~~~~~~~~~
#


class Server(object):

    def run(self):
        if DEBUG:
            DebugEngine(self).run()
        else:
            Engine(self).run()

    def match(self, environ):
        # 匹配 URL 路由，返回 (handler, kwargs)。
        handler, kwargs = Router.instance.match(environ)
        return handler and (handler, kwargs) or (not_found, {})

    def execute(self, environ, start_response, handler, kwargs):
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

        # 处理结果。
        ret = handler(**kwargs)

        if "response" in handler_args:
            return kwargs["response"](environ, start_response)
        elif not "start_response" in handler_args:
            return Response(ret)(environ, start_response)
        elif hasattr(ret, "__iter__"):
            return ret

        return (ret,)
