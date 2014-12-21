#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-11
Desc    :   需要预安装 wsgi_intercept>=0.8.1 requests>=2.5.0 模块
"""
from unittest import TestCase
import urllib
import json

try:
    import wsgi_intercept
except:
    raise ImportError(u'请安装wsgi_intercept')
from wsgi_intercept import requests_intercept
from .engine.config import settings
from .engine.support import get_django_application
from .decorator import TAG_URLS
try:
    import requests
except:
    raise ImportError(u'请安装requests')


def _call_http_request(url, method, body=None, params=None):
    '''
    print _call_http_request('https://api.github.com/search/users?q=<keyword>'.replace('<keyword>', 'testabcdefg'), "GET").text
    print _call_http_request('https://api.github.com/search/users', "GET", params={'q': 'testabcdefg'}).text
    print _call_http_request('https://api.github.com/search/users?c=test', "GET", params={'q': 'testabcdefg'}).text
    '''
    if body is not None:
        body = json.dumps(body)

    param = ''
    if params is not None:
        param = '%s%s' % ('?' if '?' not in url else '', urllib.urlencode(params))

    r = getattr(requests, method.lower())('%s%s' % (url, param), data=body)

    return r


class MockAppengine(object):

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
        self._host = "localhost"
        # 初始化配置
        settings.setup()

    instance = InstanceDescriptor()

    '''
        设置API的域名，如果跑在线上可以直接设置
        例如：set_domain("api.zqkdapi.me")  服务端口8888
        这样请求的API就变成了http://api.zqkdapi.me:8888/apixxx
        可以完全模拟服务器的WSGI environ
    '''
    def set_domain(self, host):
        self._host = host

    '''
        获取模拟请求的domain，默认为localhost
    '''
    def get_mock_api_domain(self):
        return self._host

    '''
        WSGI处理函数，修改自appengine
    '''
    def appengine_execute(self, environ, start_response):
        # 模拟appengine的运行过程
        from httpappengine.engine.router import Router
        from httpappengine.helper import not_found, server_error
        from httpappengine.engine.util import str_startswith_str_list, pdb_pm
        # 匹配 URL 路由，返回 (handler, kwargs)。
        handler, kwargs = Router.instance.match(environ)

        if handler is None:
            if settings.SUPPORT_DJANGO:
                django_application = get_django_application()

                def match_failure(environ, start_response):
                    PATH_INFO = environ.get("PATH_INFO")
                    if settings.DJANGO_URLS and not str_startswith_str_list(PATH_INFO, settings.DJANGO_URLS):
                        return not_found(start_response)
                    else:
                        ret = django_application(environ=environ, start_response=start_response)
                        # 处理结果。
                        if ret is None:
                            return server_error(start_response)
                        return ret
                return match_failure(environ, start_response)
            else:
                return server_error(start_response)

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

        # 取消调度器
        try:
            ret = handler(**kwargs)
        except:
            from httpappengine.engine.util import pdb_pm
            pdb_pm()
            return server_error(start_response)

        # 处理结果。
        if "response" in handler_args:
            return kwargs["response"](environ, start_response)
        elif not "start_response" in handler_args:
            return settings.Response(ret)(environ, start_response)
        elif hasattr(ret, "__iter__"):
            return ret

        return (ret,)

    '''
        wsgi_intercept 装载 wsgi处理函数
        使用wsgi_intercept 覆盖 requests的对外请求
    '''
    def start_mock(self):
        wsgi_intercept.add_wsgi_intercept(self._host, settings.PORT, lambda: self.appengine_execute)
        requests_intercept.install()

    '''
        还原requests
        取消wsgi_intercept装载
    '''
    def end_mock(self):
        requests_intercept.uninstall()
        wsgi_intercept.remove_wsgi_intercept()


class BaseHttpTestCase(TestCase):
    def json_loads(self, s, **kwargs):
        import json
        return json.loads(s, **kwargs)
    
    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return '%s://localhost:%s%s' % ("http", settings.PORT, path)

    def call_http_request(self, url_path, method="GET", body=None, params=None):
        return _call_http_request(self.get_url(url_path), method, body, params)

    def call_api_request(self, url_path, method="GET", body=None, params=None):
        r = self.call_http_request(url_path, method, body, params)
        return self.json_loads(r.text)

    def assertKeysIncludeDict(self, key_names, dic):
        self.assertTrue(isinstance(key_names, list))
        self.assertTrue(isinstance(dic, dict))
        for name in key_names:
            self.assertTrue(name in dic)


class AppFuncTestCase(BaseHttpTestCase):
    Func = None

    def __init__(self, methodName='runTest'):
        super(AppFuncTestCase, self).__init__(methodName)
        if not self.Func:
            raise ValueError(u'请设置需要测试的业务函数self.Func')
        # 业务函数地址，遵循werkzeug的route规则

    def get_api_uri(self):
        return getattr(self.Func, TAG_URLS).keys()[0]


def print_test_statistics(func):
    '''
        打印测试函数的调用时间 wrapper
    '''
    def wrapper(obj):
        import datetime
        d1 = datetime.datetime.now()
        func(obj)
        d2 = datetime.datetime.now()
        print "------------%s  total_seconds:%s------------" % (func.__name__, (d2-d1).total_seconds())
    return wrapper


def start_mock():
    MockAppengine.instance.start_mock()


def end_mock():
    MockAppengine.instance.end_mock()