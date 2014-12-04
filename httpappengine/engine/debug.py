# coding=utf-8

from time import sleep
from wsgiref.simple_server import make_server
from signal import signal, SIGINT
from os import walk
from os.path import join, getmtime
from threading import Thread, RLock

from .router import Router
from .config import settings
from .interface import BaseEngine
from .util import prof_call, pdb_pm, app_path, mod_path


class DebugEngine(BaseEngine):

    #
    # 调试服务器，适用于逻辑开发、调试。
    # 未做任何优化，勿用于性能测试。
    #

    def __init__(self, server):
        self._server = server
        self._lock = RLock()
        self._reload = False

        Reloader(self)
        signal(SIGINT, lambda *args: exit(0))

    def run(self):
        make_server(settings.HOST, settings.PORT, self.pre_execute).serve_forever()

    def reload(self):
        # 设置重新载入标记。
        with self._lock:
            self._reload = True

    def async_execute(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    def pre_execute(self, environ, start_response):
        # 是否使用pdb进行调试
        if settings.USE_PDB:
            try:
                return self._execute(environ, start_response)
            except:
                # 进入异常现场。
                pdb_pm()
        else:
            return self._execute(environ, start_response)


    def _execute(self, environ, start_response):
        # 刷新 Router Handler 配置。
        with self._lock:
            if self._reload:
                self._reload = False
                Router.instance.reset().load()

        # 使用 Profile 输出性能分析数据。
        print "-" * 80
        return prof_call(self._server.execute, environ, start_response)


# ------------------------------------------------------------------------ #


class Reloader(object):

    #
    # 使用多线程监控 action 目录变化。
    # 通知 DebugApplication 重新载入 Handlers。
    #

    def __init__(self, server):
        self._server = server
        self._path_list = [app_path(mod_path(mod)) for mod in settings.Action_module_list]
        self._files = self._scan()

        t = Thread(target=self._watch)
        t.daemon = True
        t.start()

    def _scan(self):
        # 扫描全部文件，返回 {filename: mtime}。
        ret = {}
        for action_path in self._path_list:
            for path, _, files in walk(action_path):
                # print path, files

                for f in files:
                    if not f.endswith(".py"):
                        continue

                    filename = join(path, f)
                    ret[filename] = getmtime(filename)

        return ret

    def _watch(self):
        # 多线程循环扫描比较。
        while True:
            sleep(1)
            new = self._scan()

            # 通过 key 对称差集来判断是否有文件新增或删除，value 则用于判断是否有修改时间变化。
            if new.viewkeys() ^ self._files.viewkeys() or set(new.values()) ^ set(self._files.values()):
                print "new file"
                self._files = new
                self._server.reload()
