# coding=utf-8

from .config import DEBUG, Engine, SUPPORT_DJANGO, DJANGO_URLS
from .router import Router
from .parser import Request, Response
from .debug import DebugEngine
from .scheduler import Scheduler
from ..helper import not_found, server_error
from .util import str_startswith_str_list


def appengine_scheduler(_engine, handler, args, kwargs):
    # 调度器
    if DEBUG:
        # 不使用 with 表达式，让pdb进入更准确的异常现场
        execute = Scheduler(_engine, handler)
        # 如果错误直接抛出异常
        return execute.__enter__()(*args, **kwargs)
    else:
        # 异常保护
        with Scheduler(_engine, handler) as execute:
            return execute(*args, **kwargs)


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

        # 调度器
        ret = appengine_scheduler(self._engine, handler, (), kwargs)

        # 处理结果。
        if ret is None:
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
    def monkey_patch_django(_engine):
        from django.core import urlresolvers

        # 覆盖RegexURLResolver，使得执行handler的时候使用engine的调度器
        class PatchRegexURLResolver(urlresolvers.RegexURLResolver):
            def resolve(self, path):
                resolver_match = super(PatchRegexURLResolver, self).resolve(path)

                def engine_callback(*args, **kwargs):
                    return appengine_scheduler(_engine, resolver_match.func, args, kwargs)
                # 重新设置callback函数
                resolver_match.func = engine_callback
                return resolver_match

        urlresolvers.RegexURLResolver = PatchRegexURLResolver

    class Server(BaseServer):
        def __init__(self):
            BaseServer.__init__(self)
            from support import get_django_application
            self.django_application = get_django_application()

        def match_failure(self, environ, start_response):
            PATH_INFO = environ.get("PATH_INFO")
            if DJANGO_URLS and not str_startswith_str_list(PATH_INFO, DJANGO_URLS):
                return not_found(start_response)
            else:
                ret = self.django_application(environ=environ, start_response=start_response)
                # 处理结果。
                if ret is None:
                    return server_error(start_response)
                return ret

else:
    class Server(BaseServer):
        pass