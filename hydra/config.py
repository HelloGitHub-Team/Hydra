#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-12 21:13
#   Desc    :   配置
import os

import yaml

from hydra.utils import init_log, make_cookie


class Config(object):
    NAME = "Hydra"

    run_mode = os.getenv(NAME.upper(), "local")
    filename = f".{run_mode}_env.yaml"
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

    with open(filepath, "r", encoding="utf8") as f:
        conf = yaml.safe_load(f)

    @classmethod
    def sentry_config(cls) -> dict:
        config = cls.conf.get("sentry", {})
        config["environment"] = cls.run_mode
        return config

    @classmethod
    def database_url(cls) -> str:
        return cls.conf["db_url"]

    @classmethod
    def wechat(cls) -> tuple:
        return (
            "wechat",
            cls.conf.get("wechat", {}).get("account", ""),
            cls.conf.get("wechat", {}).get("token", ""),
        )

    @classmethod
    def toutiao(cls) -> dict:
        return make_cookie(cls.conf.get("toutiao", {}).get("cookie", ""))

    @classmethod
    def zhihu(cls) -> dict:
        return make_cookie(cls.conf.get("zhihu", {}).get("cookie", ""))


logger = init_log(Config.NAME)
