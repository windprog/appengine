#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14/12/21
Desc    :   
"""
import os
import sys
# 确保能引用到action和httpappengine
PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

# 载入用户配置
os.environ.setdefault("APPENGINE_SETTINGS_MODULE", "config")

from httpappengine.aetest import AppFuncTestCase, start_mock
from action.hello import rest_hello

# 开始截获api
start_mock()


class HelloWorldTestCase(AppFuncTestCase):
    Func = rest_hello

    def test_success(self):
        data = self.call_api_request(self.get_api_uri(), "GET")
        self.assertKeysIncludeDict(['word_one', 'word_two'], data)