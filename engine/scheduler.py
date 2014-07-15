# coding=utf-8

from time import time
from config import THRESHOLD


# 异步标记
TAG_ASYNC = "__async__"


class Scheduler(object):

    #
    # 异步调度器策略
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 1. 每 10 秒采样一次执行时长，总计保存最后 6 次采样。
    # 2. 如果所保存的采样均超出阈值，则以异步执行。

    __slots__ = ("_handler", "_scheding", "_start")

    # 最后采样时间。
    LAST = "__sched_last__"

    # 采样间隔(秒)
    INTERVAL = 10

    # 采样列表。
    SAMPLING = "__sched_sampling__"

    # 采样长度
    SAMPLING_LEN = 6

    def __init__(self, handler):
        self._handler = handler
        self._scheding = time() - getattr(self._handler, self.LAST, 0) > self.INTERVAL

    def __enter__(self):
        if self._scheding:
            self._start = time()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._scheding:
            # 本次执行是否超出阈值。
            exceed = (time() - self._start) >= THRESHOLD

            # 最后的采样列表。
            sampling = getattr(self._handler, self.SAMPLING, tuple())
            sampling = len(sampling) >= self.SAMPLING_LEN and \
                sampling[-(self.SAMPLING_LEN - 1):] + (exceed,) or \
                sampling + (exceed,)

            # 异步策略。
            setattr(self._handler, TAG_ASYNC, all(sampling))

            # 更新采样状态。
            setattr(self._handler, self.SAMPLING, sampling)
            setattr(self._handler, self.LAST, time())

        return True  # 阻断异常
