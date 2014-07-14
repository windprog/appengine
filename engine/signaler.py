# coding=utf-8

from abc import ABCMeta, abstractmethod
from os import getpid, killpg, wait, WIFEXITED
from errno import ECHILD
from signal import signal, SIGINT, SIGTERM, SIGQUIT, SIGUSR1, SIGUSR2, SIG_IGN

#
# TODO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# gevent.signal 有问题，接收不到 TERM 信号。
#


class Signaler(object):

    __metaclass__ = ABCMeta

    #
    # Application Singal
    #
    # 父进程
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INT  : 忽略。
    # TERM : 向子进程发送 INT 退出信号。
    # USR1 : 新增工作子进程。
    #
    # 子进程
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INT,TERM : 停止接入服务，等待所有处理完成后结束子进程。
    # QUIT     : 停止接入服务，立即终止子进程。
    #

    @abstractmethod
    def fork_workers(self, num):
        pass

    @abstractmethod
    def worker_stop(self, graceful):
        pass

    def parent_execute(self):
        # 忽略信号。
        map(lambda s: signal(s, SIG_IGN), (SIGINT, SIGUSR2))

        # 向子进程广播 INT 信号。
        signal(SIGTERM, lambda *args: killpg(getpid(), SIGINT))

        # 增加子进程。
        signal(SIGUSR1, lambda *args: self.fork_workers(1))

        # 等待所有子进程退出。
        while True:
            try:
                _, status = wait()

                # 如果子进程非正常退出，新建。
                (not WIFEXITED(status)) and self.fork_workers(1)
            except OSError as ex:
                # 没有其他子进程，退出。
                if ex.errno == ECHILD:
                    break

    def worker_execute(self):
        # 忽略信号。
        map(lambda s: signal(s, SIG_IGN), (SIGUSR1, SIGUSR2))

        # 退出子进程。
        map(lambda s: signal(s, lambda *args: self.worker_stop(True)), (SIGINT, SIGTERM))
        signal(SIGQUIT, lambda *args: self.worker_stop(False))
