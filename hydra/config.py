#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-12 21:13
#   Desc    :   配置
import os

import yaml


class Config(object):
    NAME = "Hydra"

    run_mode = os.getenv("hydra_env", "local")
    filename = f".{run_mode}_env.yaml"
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

    platform = {
        "wechat": {"id": 1, "name": "wechat"},
    }
    with open(filepath, "r", encoding="utf8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    @classmethod
    def sentry_config(cls) -> dict:
        config = cls.conf["sentry"]
        config["environment"] = cls.run_mode
        return config

    @classmethod
    def database_url(cls) -> str:
        return cls.conf["db_url"]

    @classmethod
    def wechat(cls) -> tuple:
        return "wechat", cls.conf["wechat"]["account"], cls.conf["wechat"]["token"]
