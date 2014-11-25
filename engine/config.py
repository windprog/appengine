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

# Action 模块。
Action = import_module("action")

# 合并用户配置
globals().update(vars(import_module("config")))

# 各驱动实现对象。
Engine = import_module("engine.driver.engine_" + ENGINE).Engine
Selector = import_module("engine.driver.router_" + SELECTOR).Selector
Request = import_module("engine.driver.parser_" + PARSER).Request
Response = import_module("engine.driver.parser_" + PARSER).Response
