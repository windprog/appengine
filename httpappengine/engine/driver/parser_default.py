# coding=utf-8

from werkzeug.wrappers import Request as wRequest, Response as wResponse
from ..interface import BaseRequest, BaseResponse


class Request(wRequest, BaseRequest):
    pass


class Response(wResponse, BaseResponse):
    pass
