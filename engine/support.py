#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-1
Desc    :   支持各种框架，目前支持django
"""


def get_django_application():
    if "django_application" not in globals():
        import os
        from config import DJANGO_SETTINGS_MODULE
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
        #载入设置
        from django.core.wsgi import get_wsgi_application
        #django 处理wsgi的函数
        django_application = get_wsgi_application()
        globals()['django_application'] = django_application
    else:
        django_application = globals()['django_application']
    return django_application