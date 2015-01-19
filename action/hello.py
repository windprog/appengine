# coding=utf-8

from urllib2 import urlopen
from time import sleep
import multiprocessing

from httpappengine import url
from httpappengine.helper import rest


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


@url("/rest")
def rest_hello(environ, start_response):
    data = {
        'word_one': u"Hello, ",
        'word_two': u"World!"
    }

    return rest(start_response, data)


# 多进程同步例子， 使用共享内存, 类型在multiprocessing.sharedctypes.typecode_to_type
global_select_count = multiprocessing.Value('I', 0)


@url("/add", "GET")
def add(environ, start_response):
    # 快速刷新这个页面会有效果
    if not hasattr(add, "local_select_count"):
        setattr(add, "local_select_count", 1)
        print "local_select_count init"
    else:
        setattr(add, "local_select_count", getattr(add, "local_select_count")+1)

    # 获取已自增的test_count引用
    local_select_count = getattr(add, "local_select_count")
    # 共享内存变量+1
    global_select_count.value += 1

    from httpappengine.engine.router import Router
    import os
    Router.instance._selector.add("/test%s" % local_select_count, ['GET'], add)

    s = "route_rules_count:{0}, url:<a href='/test{1}'>/test{1}</a>, local_select_count:{1}, global_select_count:{2}, pid:{3}".format(
        len(Router.instance._selector._maps._rules), local_select_count, global_select_count.value, os.getpid()
    )

    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(s)))
    ])

    return s
