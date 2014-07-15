# coding=utf-8

from time import sleep
from engine import url


@url("/")
def hello(environ, start_response):
    s = "Hello, World!\n"

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s


@url("/async")
def async(environ, start_response):
    sleep(0.01)
    s = "Hello, World!\n"

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s
