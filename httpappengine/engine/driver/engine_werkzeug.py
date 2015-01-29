#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   15/1/18
Desc    :   
"""
from __future__ import print_function
from werkzeug.serving import run_simple

from ..signaler import Signaler
from ..interface import BaseEngine
from ..config import settings


class Engine(BaseEngine):

    #
    # 引擎本身只需实现 BaseEngine 接口
    #

    def __init__(self, server):
        self._server = server
        self._listen_sock = None
        self._wsgi_server = None

        BaseEngine.__init__(self, server)
        Signaler.__init__(self)

    def run(self):
        try:
            import werkzeug.serving

            def none_log(*args, **kwargs):
                # 强制不print 输出访问log
                pass
            setattr(werkzeug.serving.WSGIRequestHandler, "log", none_log)
        except:
            pass
        if settings.SUPPORT_WEBSOCKET:
            print(u"werkzeug方式不支持运行websocket")
            raise
        run_simple(settings.HOST, settings.PORT, self._server.execute, threaded=True)

    def async_execute(self, func, *args, **kwargs):
        return func(*args, **kwargs)
