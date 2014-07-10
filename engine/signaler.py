# coding=utf-8

from os import getpid, killpg
from signal import signal, SIGINT, SIGTERM, SIGQUIT, SIG_IGN


#
# gevent.signal 有问题，接收不到 SIGTERM 信号。
#


class Signaler(object):

    #
    # Application Singal
    #
    # 父进程
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INT  : 忽略。
    # TERM : 向子进程发送 INT 退出信号。
    #
    # 子进程
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INT,TERM : 停止接入服务，等待所有处理完成后结束子进程。
    # QUIT     : 停止接入服务，立即终止子进程。
    #

    def __init__(self):
        pass

    def parent_signal(self):
        signal(SIGINT, SIG_IGN)
        signal(SIGTERM, lambda *args: killpg(getpid(), SIGINT))

    def child_signal(self, shutdown, graceful_shutdown):
        graceful_shutdown and map(lambda s: signal(s, graceful_shutdown), (SIGINT, SIGTERM))
        shutdown and signal(SIGQUIT, shutdown)
