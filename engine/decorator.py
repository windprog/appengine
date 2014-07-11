# coding=utf-8


TAG_URLS = "__urls__"
TAG_ASYNC = "__async__"

#
# TODO
# ~~~~~~~~
#


def url(path, methods="GET"):
    # 添加 urls 标记。
    def set(cls):
        if not hasattr(cls, TAG_URLS):
            setattr(cls, TAG_URLS, {})

        s = isinstance(methods, str) and methods.split(",") or methods
        getattr(cls, TAG_URLS)[path] = s
        return cls

    return set


def async(func):
    # 添加 async 标记。
    setattr(func, TAG_ASYNC, True)
    return func
