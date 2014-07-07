# coding=utf-8

import time
from engine import url, async


def test():
    time.sleep(0.01)
    return "Hello, World!\n"


@async
@url("/")
def handler(environ, start_response):
    s = test()

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s


@url("/uid/<uid>")
def uid(request, response, uid):
    print request
    response.set_cookie("a", "b")
    response.set_data(uid)
