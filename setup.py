#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 windpro

Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   14-12-1
Desc    :   
"""
from setuptools import setup

from appengine import __version__, __author__, __description__


setup(
    name="http_appengine",
    version=__version__,
    description=__description__,
    url="https://github.com/windprog/appengine",
    author=__author__,
    author_email="windprog@gmail.com",
    packages=['appengine', 'appengine.engine', 'appengine.engine.driver'],
    # package_data = {
    #     'appengine': ['engine/*.py'],
    # },
    install_requires=['gevent>=1.0.1', 'Werkzeug>=0.9.6']
)