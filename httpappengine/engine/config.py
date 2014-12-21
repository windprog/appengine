# coding=utf-8

#
# 系统配置文件
#
# 该配置会被环境变量APPENGINE_SETTINGS_MODULE 的设置文件覆盖，默认值为"config"，是根目录的config.py
# 不建议直接修改本文件。
#
from multiprocessing import cpu_count
from importlib import import_module
import os
from .. import __title__


ENVIRONMENT_VARIABLE = "APPENGINE_SETTINGS_MODULE"


class settings(object):
    # 调试开关
    # 调试状态使用 DebugApplication，可输出 profile 信息，
    # 并在出错时，使用 pdb 进入异常现场。便于调试!
    DEBUG = False

    # 在调试状态使用PDB进行调试
    USE_PDB = True

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

    # 是否支持django
    SUPPORT_DJANGO = False

    # Django相关配置，在SUPPORT_DJANGO == True时生效
    # django环境变量
    DJANGO_SETTINGS_MODULE = "django_setting.settings"
    # 支持django的url列表
    # 如果为空: engine匹配失败交给django处理
    # 非空:    其中一个字符串满足从第一个字符开始相同则交给django处理
    DJANGO_URLS = []

    # 需要载入的Action 模块默认值。
    ACTIONS = [
        "action",
        #"plugs.qiniudn"
    ]


    # --- 以下内容请勿修改 --------------------------------------------------------- #

    # CPU Core 数量。
    CPUS = cpu_count()

    # 各驱动实现对象, 默认值，必须运行setup类函数载入对象。
    Engine = None
    Selector = None
    Request = None
    Response = None

    # Action模块默认值
    Action_module_list = []


    @classmethod
    def load_module_sub(cls, sub_name):
        return import_module("%s.engine.%s" % (__title__, sub_name))

    @classmethod
    def setup(cls):
        #载入用户配置
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        # 默认载入根目录的config.py
        if settings_module:
            try:
                mod = import_module(settings_module)
            except ImportError as e:
                raise ImportError(
                    "Could not import settings '%s' (Is it on sys.path? Is there an import error in the settings file?): %s"
                    % (settings_module, e)
                )
            # 合并用户配置
            for k, v in vars(mod).iteritems():
                #跳过内部对象
                if k.startswith("__") and k.endswith("__"):
                    continue
                setattr(settings, k, v)
        else:
            # 配置不存在，载入默认配置
            print 'error, not found settings file, use default settings.'

        # 预设django config
        if settings.SUPPORT_DJANGO:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings.DJANGO_SETTINGS_MODULE)

        # 各驱动实现对象。
        cls.Engine = cls.load_module_sub("driver.engine_" + cls.ENGINE).Engine
        cls.Selector = cls.load_module_sub("driver.router_" + cls.ENGINE).Selector
        cls.Request = cls.load_module_sub("driver.parser_" + cls.ENGINE).Request
        cls.Response = cls.load_module_sub("driver.parser_" + cls.ENGINE).Response

        # Action模块载入
        cls.Action_module_list = [import_module(item) for item in cls.ACTIONS]

    @classmethod
    def setup_ready(cls):
        return True if cls.Engine else False