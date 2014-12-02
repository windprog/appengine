#!/usr/bin/env python
# coding=utf-8
import os
from httpappengine.util import run_server

os.environ.setdefault("APPENGINE_SETTINGS_MODULE", "config")

run_server()