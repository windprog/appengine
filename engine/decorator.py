# coding=utf-8


TAG_URLS = "__urls__"


def url(path, methods="GET"):
    # 添加 urls 标记。
    def set(cls):
        if not hasattr(cls, TAG_URLS):
            setattr(cls, TAG_URLS, {})

        s = isinstance(methods, str) and methods.split(",") or methods
        getattr(cls, TAG_URLS)[path] = s
        return cls

    return set
