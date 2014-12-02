#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-2
Desc    :   
"""


def run_server():
    # 在引入engine模块前，必须设置环境变量 APPENGINE_SETTINGS_MODULE 更改默认配置
    import os
    if "APPENGINE_SETTINGS_MODULE" not in os.environ:
        raise ImportError(
            "Could not import settings from env:APPENGINE_SETTINGS_MODULE."
        )
    from .engine import Server, Welcome

    Welcome()
    Server().run()