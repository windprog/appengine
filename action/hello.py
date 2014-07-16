# coding=utf-8

from urllib2 import urlopen
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
    sleep(0.2)
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
