# coding=utf-8

import time
from engine import url, async


def test():
    return "Hello, World!\n"


def block_test():
    time.sleep(0.01)
    return "Hello, World!\n"


@url("/")
def hello(environ, start_response):
    s = test()

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s


@async
@url("/async")
def hello_async(environ, start_response):
    s = block_test()

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s
