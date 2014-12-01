#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-1
Desc    :   django的url配置
"""
from django.conf.urls import *
from views import *

urlpatterns = patterns(
    'django_demo.views',
    url(r'^demo$', 'hello'),
)