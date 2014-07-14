# coding=utf-8

from time import time
from config import THRESHOLD

SCHED_ASYNC = "__scheduler_async__"
TAG_ASYNC = "__async__"


class Scheduler(object):

    #
    # 调度器
    #

    def __new__(cls, *args, **kwargs):
        o = getattr(cls, "__instance__", None)
        if not o:
            o = object.__new__(cls)
            cls.__instance__ = o

        return o

    def __init__(self, handler):
        self._handler = handler
        self._sched_async = hasattr(self._handler, SCHED_ASYNC)

    def __enter__(self):
        # 异步调度检查。
        if not self._sched_async:
            self._start = time()

    def __exit__(self, exc_type, exc_value, traceback):
        # 异步调度标记。
        if not self._sched_async:
            setattr(self._handler, SCHED_ASYNC, True)
            (time() - self._start >= THRESHOLD) and setattr(self._handler, TAG_ASYNC, True)

        return True  # 阻断异常
