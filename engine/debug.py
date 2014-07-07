# coding=utf-8

from time import time
from wsgiref.simple_server import make_server

from config import HOST, PORT

# TODO:
# 1. 使用 Thread 定期扫描文件修改时间，Auto-Reload。


class DebugApplication(object):
    # 调试服务器，适用于逻辑开发、调试。
    # 未做任何优化，勿用于性能测试。

    def __init__(self, server):
        self._server = server

    def _execute(self, environ, start_response):
        try:
            start = time()

            handler, kwargs = self._server.match(environ)
            ret = self._server.execute(environ, start_response, handler, kwargs)

            # 输出执行时间，以便决定是否使用异步调用。
            end = time() - start
            print "[{0}.{1}] {2}s".format(handler.__module__, handler.__name__, end)

            return ret
        except:
            # 使用 pdb 进入异常现场。
            try:
                pdb = __import__("ipdb")
            except:
                import pdb

            import sys
            import traceback
            _, _, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)

    def run(self):
        make_server(HOST, PORT, self._execute).serve_forever()
