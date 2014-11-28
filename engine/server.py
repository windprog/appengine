# coding=utf-8

from config import DEBUG, Engine, SUPPORT_DJANGO, DJANGO_SETTINGS_MODULE, DJANGO_URLS
from router import Router
from parser import Request, Response
from debug import DebugEngine
from scheduler import Scheduler
from helper import not_found, server_error
from util import str_startswith_str_list


class BaseServer(object):

    def __init__(self):
        self._engine = DEBUG and DebugEngine(self) or Engine(self)

    def run(self):
        self._engine.run()

    def execute(self, environ, start_response):
        # 匹配 URL 路由，返回 (handler, kwargs)。
        handler, kwargs = Router.instance.match(environ)

        if handler is None:
            return self.match_failure(environ, start_response)
        else:
            return self.match_success(environ, start_response, handler, kwargs)

    def match_success(self, environ, start_response, handler, kwargs):
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

        # 调度器 (异常保护)
        with Scheduler(self._engine, handler) as execute:
            ret = execute(**kwargs)

        # 处理结果。
        if "ret" not in locals():
            return server_error(start_response)
        elif "response" in handler_args:
            return kwargs["response"](environ, start_response)
        elif not "start_response" in handler_args:
            return Response(ret)(environ, start_response)
        elif hasattr(ret, "__iter__"):
            return ret

        return (ret,)

    def match_failure(self, environ, start_response):
        return not_found(start_response)


if SUPPORT_DJANGO:
    class Server(BaseServer):
        def __init__(self):
            BaseServer.__init__(self)
            import os
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
            #载入设置
            from django.core.wsgi import get_wsgi_application
            #django 处理wsgi的函数
            self.django_application = get_wsgi_application()

        def match_failure(self, environ, start_response):
            PATH_INFO = environ.get("PATH_INFO")
            if DJANGO_URLS and not str_startswith_str_list(PATH_INFO, DJANGO_URLS):
                return not_found(start_response)
            else:
                return self.django_application(environ=environ, start_response=start_response)

else:
    class Server(BaseServer):
        pass