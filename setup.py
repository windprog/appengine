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

from httpappengine import __version__, __author__, __description__


setup(
    name="httpappengine",
    version=__version__,
    description=__description__,
    url="https://github.com/windprog/appengine",
    author=__author__,
    author_email="windprog@gmail.com",
    packages=['httpappengine', 'httpappengine.engine', 'httpappengine.engine.driver'],
    install_requires=['gevent>=1.0.1', 'Werkzeug>=0.9.6']
)