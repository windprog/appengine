# coding=utf-8

from sys import argv, modules
from os.path import dirname, abspath, join
from importlib import import_module
from pkgutil import walk_packages
from inspect import getmembers


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
    try:
        pdb = __import__("ipdb")
    except:
        import pdb

    from sys import exc_info
    from traceback import print_exc

    _, _, tb = exc_info()
    print_exc()
    pdb.post_mortem(tb)


def prof_call(func, *args):
    # 输出函数调用性能分析。
    from cProfile import Profile
    from pstats import Stats

    prof = Profile(builtins=False)
    ret = prof.runcall(func, *args)
    Stats(prof).sort_stats("cumtime").print_stats("(/engine/)|(/action/)", 10)
    return ret
