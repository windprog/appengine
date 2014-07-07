# coding=utf-8

from importlib import import_module
from pkgutil import walk_packages
from inspect import getmembers


def singleton(cls):
    def wrap(*args, **kwargs):
        o = getattr(cls, "__instance__", None)
        if not o:
            o = cls(*args, **kwargs)
            cls.__instance__ = o

        return o
    return wrap


def walk_members(package, predicate, callback):
    for _, name, ispkg in walk_packages(package.__path__, package.__name__ + "."):
        if ispkg:
            continue

        m = import_module(name)
        handlers = getmembers(m, predicate)
        map(callback, (h for _, h in handlers))
