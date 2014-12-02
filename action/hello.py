# coding=utf-8

from urllib2 import urlopen
from time import sleep
from appengine.engine import url


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


@url("/remote")
def remote(environ, start_response):
    s = urlopen("http://220.181.40.167:8080").read()

    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(s)))
    ])

    return s

@url("/add", "GET")
def add(environ, start_response):
    if not hasattr(add, "test_count"):
        test_count = 0
        setattr(add, "test_count", test_count)
        print "set"
    else:
        test_count = getattr(add, "test_count")
        setattr(add, "test_count", test_count+1)

    from appengine.router import Router
    import os
    Router.instance._selector.add("/test%s" % test_count, ['GET'], add)

    s = "<a href='/test%s'>test%s, select_count:%s, pid:%s</a>" % (
        test_count, test_count, len(Router.instance._selector._maps._rules), os.getpid())

    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(s)))
    ])

    return s