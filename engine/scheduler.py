# coding=utf-8

from time import time
from collections import defaultdict
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

    async = dict()  # 异步标志
    last = defaultdict(lambda: 0)  # 最后调度时间
    samples = defaultdict(tuple)  # 采样列表

    def __init__(self, engine, handler):
        self._engine = engine
        self._handler = handler

    def __enter__(self):
        self._start = time()
        return self.async.get(self._handler, self._handler)

    def __exit__(self, exc_type, exc_value, traceback):
        if self._start - self.last[self._handler] >= 60:  # 1 分钟
            # 最后的采样列表。
            exceed = (time() - self._start) >= THRESHOLD
            samples = self.samples[self._handler][-5:] + (exceed,)

            # 更新状态。
            self.samples[self._handler] = samples
            self.last[self._handler] = self._start

            # 异步决策。
            e = self._handler in self.async

            if all(samples):
                if not e:
                    self.async[self._handler] = partial(self._engine.async_execute, self._handler)
            elif e:
                del self.async[self._handler]

        return True  # 阻断异常


class Scheduler2(object):

    #
    # 异步调度器策略
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 1. 每 1 分钟采样一次执行时长，总计保存最后 6 次采样。
    # 2. 如果所保存的采样均超出阈值，则以异步执行。
    #

    __slots__ = ("_engine", "_handler")

    async = dict()  # 异步标志
    last = defaultdict(lambda: 0)  # 最后调度时间
    samples = defaultdict(tuple)  # 采样列表

    def __init__(self, engine, handler):
        self._engine = engine
        self._handler = handler

    def __enter__(self):
        return time() - self.last[self._handler] >= 60 and \
            self._sample or \
            self.async.get(self._handler, self._handler)

    def __exit__(self, exc_type, exc_value, traceback):
        # 阻断异常 (TODO:日志?)
        return True

    def _sample(self, *args, **kwargs):
        start = time()

        # 使用包裹函数返回精确执行时间采样。
        def wrap(*args, **kwargs):
            ret = self._handler(*args, **kwargs)
            return ret, time() - start

        e = self._handler in self.async
        ret, exceed = e and self._engine.async_execute(wrap, *args, **kwargs) or wrap(*args, **kwargs)

        # 最后的采样列表。
        samples = self.samples[self._handler][-5:] + (exceed >= THRESHOLD,)

        # 更新状态。
        self.samples[self._handler] = samples
        self.last[self._handler] = start

        # 异步决策。
        if all(samples):
            if not e:
                self.async[self._handler] = partial(self._engine.async_execute, self._handler)
        elif e:
            del self.async[self._handler]

        return ret
