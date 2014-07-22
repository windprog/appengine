# coding=utf-8

from time import time
from collections import defaultdict
from functools import partial

from config import THRESHOLD


class Scheduler(object):

    #
    # 异步调度策略
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 1. 每 1 分钟采样一次执行时长，总计保存最后 6 次采样。
    # 2. 如果所保存的采样均超出阈值，则以异步执行。
    #

    __slots__ = ("_engine", "_handler")

<<<<<<< HEAD
    async = set()  # 异步标志
    last = defaultdict(lambda: 0)  # 最后调度时间
=======
    async = dict()  # 异步标志
    last = defaultdict(lambda: 0)  # 最后采样时间
>>>>>>> dc8d9e94d8ee92500f4b1141971930fa5bd3e299
    samples = defaultdict(tuple)  # 采样列表

    def __init__(self, engine, handler):
        self._engine = engine
        self._handler = handler

    def __enter__(self):
<<<<<<< HEAD
        execute = self._handler in self.async and \
            partial(self._engine.async_execute, self._handler) or \
            self._handler

        self._start = time()
        return execute

    def __exit__(self, exc_type, exc_value, traceback):
        if self._start - self.last[self._handler] >= 60:  # 1 分钟
            # 本次执行是否超出阈值。
            exceed = (time() - self._start) >= THRESHOLD

            # 最后的采样列表。
            samples = self.samples[self._handler]
            samples = len(samples) >= 6 and samples[-5:] + (exceed,) or samples + (exceed,)

            # 更新状态。
            all(samples) and self.async.add(self._handler) or self.async.discard(self._handler)
            self.samples[self._handler] = samples
            self.last[self._handler] = self._start

        return True  # 阻断异常
=======
        return time() - self.last[self._handler] >= 60 and \
            self._sample or \
            self.async.get(self._handler, self._handler)

    def __exit__(self, exc_type, exc_value, traceback):
        # 阻断异常 (TODO:日志?)
        return True

    def _sample(self, *args, **kwargs):
        # 使用包裹函数返回精确执行时间采样。
        def wrap(*args, **kwargs):
            start = time()
            ret = self._handler(*args, **kwargs)
            return ret, time() - start

        e = self._handler in self.async
        ret, exceed = e and self._engine.async_execute(wrap, *args, **kwargs) or wrap(*args, **kwargs)

        # 采样列表。
        samples = self.samples[self._handler][-5:] + (exceed >= THRESHOLD,)

        # 异步决策。
        if all(samples):
            if not e:
                self.async[self._handler] = partial(self._engine.async_execute, self._handler)
        elif e:
            del self.async[self._handler]

        # 更新状态。
        self.samples[self._handler] = samples
        self.last[self._handler] = time()

        return ret
>>>>>>> dc8d9e94d8ee92500f4b1141971930fa5bd3e299
