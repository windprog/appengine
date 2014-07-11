# coding=utf-8

from sys import argv, modules, exc_info
from os.path import dirname, abspath, join
from importlib import import_module
from pkgutil import walk_packages
from inspect import getmembers
from traceback import print_exc
from cProfile import Profile
from pstats import Stats


try:
    pdb = __import__("ipdb")
except:
    import pdb


def app_path(sub):
    # 返回应用子目录绝对路径。
    return join(dirname(abspath(argv[0])), sub)


def walk_members(package, predicate, callback):
    # 遍历包中所有模块成员。
    for _, name, ispkg in walk_packages(package.__path__, package.__name__ + "."):
        if ispkg:
            continue

        if name in modules:
            reload(modules[name])

        m = import_module(name)
        members = getmembers(m, predicate)
        map(callback, (m for _, m in members))


def pdb_pm():
    # 使用 pdb 进入异常现场。
    _, _, tb = exc_info()
    print_exc()
    pdb.post_mortem(tb)


def prof_call(func, *args):
    # 输出函数调用性能分析。
    prof = Profile(builtins=False)
    ret = prof.runcall(func, *args)
    Stats(prof).sort_stats("time").print_stats("(/engine/)|(/action/)", 10)
    return ret


def max_key_length(iterator, key):
    # 计算最宽 key 长度。
    def f(a, v):
        n = len(key(v))
        return a > n and a or n

    return reduce(f, iterator, 0)


def http_methods_flag(*methods):
    # 按标志位输出 HTTP methods 标记。
    flags = (("get", "g"), ("post", "p"), ("put", "u"),
             ("delete", "d"), ("head", "h"), ("options", "o"))

    methods = map(lambda m: m.lower(), methods)
    return "".join(map(lambda (m, f): m in methods and f or "-", flags))
