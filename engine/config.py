# coding=utf-8

DEBUG = True

HOST = "0.0.0.0"
PORT = 8888
WORKERS = 0

ENGINE = "default"
SELECTOR = "default"
PARSER = "default"


# ------------------------------------------------------------ #


from multiprocessing import cpu_count
from importlib import import_module

# 动态配置
CPUS = cpu_count()

Action = import_module("action")
Application = import_module("engine.driver.engine_" + ENGINE).Application
Selector = import_module("engine.driver.router_" + SELECTOR).Selector
Request = import_module("engine.driver.parser_" + PARSER).Request
Response = import_module("engine.driver.parser_" + PARSER).Response

# 合并用户配置
globals().update(vars(import_module("config")))
