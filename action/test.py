# coding=utf-8

from engine import url


@url("/abc")
def abc(*args, **kwargs):
    return "abc"
