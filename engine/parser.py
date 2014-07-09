# coding=utf-8

from config import Request, Response

# TODO: 提供通用 Request、Response 接口，使其不再依赖 Driver 实现。

#
#  Request Driver Interface
#  -----------------------------------------
#  class Request:
#      def __init__(self, environ): pass
#

#
#  Response Driver Interface
#  -------------------------------------------------------
#  class Response:
#      def __init__(self): pass
#      def __call__(self, environ, start_response): pass
#      def set_data(self, data): pass
#
