# coding=utf-8

from __future__ import print_function

from server import Server
from decorator import async, url

__all__ = ["Server", "async", "url", "Welcome"]


def Welcome():
    # 输出欢迎信息。

    from config import options
    from router import Router

    def pprint(iterator, title, key, callback):
        # 格式化输出信息。

        def max_length(iterator, key):
            # 计算合适宽度。
            def f(a, v):
                n = len(key(v))
                return a > n and a or n

            return reduce(f, iterator, 0)

        print("\n=== {0} ===\n".format(title))
        d = sorted(iterator, key=key)
        n = max_length(d, key)
        map(lambda v: callback(v, n), d)

    # 配置信息。
    pprint(options.iteritems(),
           "Options",
           lambda (k, v): k,
           lambda v, n: print("  {0} : {1}".format(v[0].ljust(n), v[1])))

    # Handlers 信息。
    d = (("{0}.{1}".format(h.__module__, h.__name__), u, hasattr(h, "__async__") and "*" or " ")
         for u, h in Router.instance.handlers.iteritems())

    pprint(d,
           "Handlers",
           lambda (h, u, a): h,
           lambda v, n: print(" {2}{0} : {1}".format(v[0].ljust(n), v[1], v[2])))

    print()
