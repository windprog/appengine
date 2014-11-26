# coding=utf-8

#
# 系统配置文件
#
# 该配置会被根目录下 config.py 中同名设置覆盖。
# 不建议直接修改本文件。
#

# 调试开关
# 调试状态使用 DebugApplication，可输出 profile 信息，
# 并在出错时，使用 pdb 进入异常现场。便于调试!
DEBUG = False

# 服务器监听地址。
HOST = "0.0.0.0"
PORT = 8888

# 建议工作进程数量。
# 由具体的 Engine-Driver 决定是否采用。
# 为 0 时表示由 Engine-Driver 决定工作进程数量。
WORKERS = 0

# Engine 驱动名称。
ENGINE = "default"

# Router Selector 驱动名称。
SELECTOR = "default"

# Request、Response 解析器驱动名称。
PARSER = "default"

# HTTPS
# 文件存放于项目目录的 ssl/ 子目录下
HTTPS = False
HTTPS_KEY = "server.key"
HTTPS_CERT = "server.crt"

# 调度器异步阈值(秒)。
THRESHOLD = 0.01


# --- 以下内容请勿修改 --------------------------------------------------------- #


from multiprocessing import cpu_count
from importlib import import_module

# CPU Core 数量。
CPUS = cpu_count()

ENVIRONMENT_VARIABLE = "APPENGINE_SETTINGS_MODULE"

# 需要载入的Action 模块默认值。
ACTIONS = [
    "action",
    #"plugs.qiniudn"
]


def load_config():
    import os
    settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
    # 默认载入根目录的config.py
    if not settings_module:
        settings_module = "config"
    try:
        mod = import_module(settings_module)
    except ImportError as e:
        raise ImportError(
            "Could not import settings '%s' (Is it on sys.path? Is there an import error in the settings file?): %s"
            % (settings_module, e)
        )
    # 合并用户配置
    globals().update(vars(mod))

# 获取用户配置
load_config()

# Action模块载入
Action_module_list = [import_module(item) for item in ACTIONS]


# 各驱动实现对象。
Engine = import_module("engine.driver.engine_" + ENGINE).Engine
Selector = import_module("engine.driver.router_" + SELECTOR).Selector
Request = import_module("engine.driver.parser_" + PARSER).Request
Response = import_module("engine.driver.parser_" + PARSER).Response
