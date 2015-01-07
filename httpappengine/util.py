#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-2
Desc    :   常用外部方法
"""
from .decorator import TAG_URLS


def run_server():
    from .engine import Server, Welcome

    server = Server()

    Welcome()

    server.run()


def get_action_uri(func):
    return getattr(func, TAG_URLS).keys()[0]