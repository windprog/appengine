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