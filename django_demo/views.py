#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-1
Desc    :   django的views，内含 hello world
"""
from django.http import HttpResponse


def hello(request):
    import os
    s = "<a href='/demo'>hello world!, pid:%s</a>" % (
        os.getpid()
    )
    return HttpResponse(s)