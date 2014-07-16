# coding=utf-8

from time import time
from functools import partial

from config import THRESHOLD


class Scheduler(object):

    #
    # 异步调度器策略
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 1. 每 1 分钟采样一次执行时长，总计保存最后 6 次采样。
    # 2. 如果所保存的采样均超出阈值，则以异步执行。
    #
    #
    # TODO
    # ~~~~~~~~~~~~~~~~~~~~~~~
    # 因为 engine 可能以 coroutine/threadpool 方式执行，所以会存在多个 Scheduler，因此不能用单例。
    # 测量时长，可能是 coroutine/threadpool 造成的，应该改进采样方式。
    #

    __slots__ = ("_engine", "_handler", "_start")

    ASYNC = "__async__"
    LAST = "__last__"
    SAMPLES = "__samples__"

    def __init__(self, engine, handler):
        self._engine = engine
        self._handler = handler

    def __enter__(self):
        execute = hasattr(self._handler, self.ASYNC) and \
            partial(self._engine.async_execute, self._handler) or \
            self._handler

        self._start = time()
        return execute

    def __exit__(self, exc_type, exc_value, traceback):
        if self._start - getattr(self._handler, self.LAST, 0) >= 60:  # 1 分钟
            # 本次执行是否超出阈值。
            exceed = (time() - self._start) >= THRESHOLD

            # 最后的采样列表。
            samples = getattr(self._handler, self.SAMPLES, tuple())
            samples = len(samples) >= 6 and samples[-5:] + (exceed,) or samples + (exceed,)

            # 更新状态。
            setattr(self._handler, self.ASYNC, all(samples))
            setattr(self._handler, self.SAMPLES, samples)
            setattr(self._handler, self.LAST, self._start)

        return True  # 阻断异常
