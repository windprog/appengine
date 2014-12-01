# coding=utf-8
# 详细配置说明请参考engine/config.py
DEBUG = True

# 服务器监听地址。
HOST = "0.0.0.0"
PORT = 8888

# 需要载入的Action 模块
ACTIONS = [
    "action",
    #"plugs.qiniudn"
]

SUPPORT_DJANGO = True
DJANGO_SETTINGS_MODULE = "django_demo.settings"
DJANGO_URLS = [
    # "/demo"
]

USE_PDB = True