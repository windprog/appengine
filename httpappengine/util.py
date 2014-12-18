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
    from .engine import Server, Welcome

    server = Server()

    Welcome()

    server.run()


def exc_check():
    # 在业务函数处理异常， 非debug模式不会触发pdb
    from pdb import post_mortem
    from sys import exc_info
    from traceback import print_exc
    from .engine.config import settings
    _, _, tb = exc_info()
    print_exc()
    if settings.USE_PDB and settings.DEBUG:
        post_mortem(tb)