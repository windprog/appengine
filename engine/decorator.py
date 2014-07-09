# coding=utf-8


def url(*paths):
    # 添加 __urls__ 标记。
    def set(cls):
        if not hasattr(cls, "__urls__"):
            cls.__urls__ = []

        cls.__urls__.extend(paths)
        return cls

    return set


def async(func):
    # 异步装饰器
    func.__async__ = True
    return func
