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

from httpappengine.aetest import BaseHttpTestCase, start_mock
from httpappengine.util import get_action_uri
from action.hello import rest_hello

# 开始截获testcase, 将会直接经由wsgi模块调用业务函数,不经过socket发起远端request
start_mock()


class HelloWorldTestCase(BaseHttpTestCase):
    def test_success(self):
        data = self.call_json_request(get_action_uri(rest_hello), "GET")
        self.assertKeysIncludeDict(['word_one', 'word_two'], data)

if __name__ == '__main__':
    import unittest
    unittest.main()