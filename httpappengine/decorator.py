# coding=utf-8


TAG_URLS = "__urls__"
TAG_FUNC = "__func__"


def url(path, methods="GET"):
    # 添加 urls 标记。
    def set(cls):
        if not hasattr(cls, TAG_URLS):
            setattr(cls, TAG_URLS, {})

        s = isinstance(methods, str) and methods.split(",") or methods
        getattr(cls, TAG_URLS)[path] = s
        return cls

    return set


def parse_wrapper_return(wrapper_func):
    # 添加 func 标记，使得框架刚开始运行的时候输出的接口列表信息正确
    # 这个修饰器不是必须使用的。
    #
    # 原理为在函数对象中增加一个属性:__func__  值为业务函数。
    # 这样在输出调试信息的时候就是根据这个__func__字段输出业务函数名称
    def wrapper(sour_func):
        des_func = wrapper_func(sour_func)
        if not hasattr(des_func, TAG_FUNC):
            setattr(des_func, TAG_FUNC, sour_func)
        return des_func
    return wrapper