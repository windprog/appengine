# coding=utf-8

from engine import url


@url("/abc")
def abc(*args, **kwargs):
    return "abc"


@url("/uid/<uid>")
def uid(request, response, uid):
    print request
    response.set_cookie("a", "b")
    response.set_data(uid)
