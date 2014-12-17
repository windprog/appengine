# coding=utf-8

from .config import settings
from .router import Router
from .debug import DebugEngine
from .scheduler import Scheduler
from ..helper import not_found, server_error

SERVER_ERROR = -1


def appengine_scheduler(_engine, handler, args, kwargs):
    # 调度器
    if settings.DEBUG:
        # 不使用 with 表达式，让pdb进入更准确的异常现场
        execute = Scheduler(_engine, handler)
        # 如果错误直接抛出异常
        return execute.__enter__()(*args, **kwargs)
    else:
        # 异常保护
        with Scheduler(_engine, handler) as execute:
            ret = execute(*args, **kwargs)
            # 返回值不能为SERVER_ERROR
            assert ret != SERVER_ERROR
            return ret
        return SERVER_ERROR


class BaseServer(object):

    def __init__(self):
        # 在引入engine模块前，必须设置环境变量 APPENGINE_SETTINGS_MODULE 更改默认配置
        import os
        if "APPENGINE_SETTINGS_MODULE" not in os.environ:
            raise ImportError(
                "Could not import settings from env:APPENGINE_SETTINGS_MODULE."
            )
        settings.setup()
        self._engine = settings.DEBUG and DebugEngine(self) or settings.Engine(self)

    def run(self):
        from gevent.monkey import patch_socket, patch_ssl
        patch_socket()
        # 在patch socket之后，如果使用https会出错，需要连ssl也patch掉
        patch_ssl()
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
            kwargs["request"] = settings.Request(environ)
        if "response" in handler_args:
            kwargs["response"] = settings.Response()

        # 调度器
        ret = appengine_scheduler(self._engine, handler, (), kwargs)

        # 处理结果。
        if ret == SERVER_ERROR:
            return server_error(start_response)
        elif "response" in handler_args:
            return kwargs["response"](environ, start_response)
        elif not "start_response" in handler_args:
            return settings.Response(ret)(environ, start_response)
        elif hasattr(ret, "__iter__"):
            return ret

        return (ret,)

    def match_failure(self, environ, start_response):
        return not_found(start_response)


class Server(BaseServer):
    def __init__(self):
        BaseServer.__init__(self)
        #支持django
        if settings.SUPPORT_DJANGO:
            from support import patch_django
            patch_django(self, self._engine)