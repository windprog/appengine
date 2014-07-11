# coding=utf-8

from os import getpid, killpg
from signal import signal, SIGINT, SIGTERM, SIGQUIT, SIGUSR1, SIGUSR2, SIG_IGN

#
# TODO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# gevent.signal 有问题，接收不到 TERM 信号。
#


class Signaler(object):

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

    def __init__(self):
        pass

    def parent_signal(self, fork_workers=None):
        # 忽略信号。
        map(lambda s: signal(s, SIG_IGN), (SIGINT, SIGUSR1, SIGUSR2))

        # 向子进程广播 INT 信号。
        signal(SIGTERM, lambda *args: killpg(getpid(), SIGINT))

        # 增加子进程。
        fork_workers and signal(SIGUSR1, lambda *args: fork_workers(1))

    def worker_signal(self, stop_worker=None):
        # 忽略信号。
        map(lambda s: signal(s, SIG_IGN), (SIGUSR1, SIGUSR2))

        # 退出子进程。
        if stop_worker:
            map(lambda s: signal(s, lambda *args: stop_worker()), (SIGINT, SIGTERM))
            signal(SIGQUIT, lambda *args: stop_worker(False))
