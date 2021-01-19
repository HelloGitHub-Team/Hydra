#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-05 21:47
#   Desc    :
import base64
import datetime
import os
import re
import time
from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from os import path

import requests

from hydra.config import Config

# requests.packages.urllib3.disable_warnings()


def init_log(name, log_type=None):
    log_path = os.path.join(path.dirname(path.dirname(__file__)), "logs/")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if log_type == "time":
        handler = TimedRotatingFileHandler(
            os.path.join(log_path, "{}.log".format(name)),
            when="midnight",
            backupCount=10,
            encoding="utf-8",
        )
    else:
        handler = RotatingFileHandler(
            os.path.join(log_path, "{}.log".format(name)), encoding="utf-8"
        )
    log_object = getLogger(name)
    formatter = Formatter("%(name)s %(module)s  %(asctime)s %(levelname)s %(message)s")
    stream_hdr = StreamHandler()
    stream_hdr.setFormatter(formatter)
    log_object.addHandler(stream_hdr)
    log_object.setLevel(DEBUG)
    handler.setFormatter(formatter)
    log_object.addHandler(handler)
    return log_object


class BaseSpider(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.log = init_log(Config.NAME)  # 设置log名称
        self.token_header = {}

    @property
    def today(self):
        return datetime.date.today()

    def request_data(self, method="GET", **kwargs):
        url = kwargs.pop("url")
        if not kwargs.get("timeout"):
            kwargs["timeout"] = 20
        # 过滤敏感信息，防止打到日志中
        args_list = []
        for k, v in kwargs.items():
            if k == "auth":
                continue
            if isinstance(v, dict) and (("Authorization" in v) or ("token" in v)):
                continue
            args_list.append("{}: {}".format(k, v))
        args_str = "{" + ",".join(args_list) + "}"
        try:
            s_time = time.time()
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            else:
                response = requests.post(url, **kwargs)
            speed_time = round(time.time() - s_time, 2)
            r_limit = response.headers.get("X-RateLimit-Remaining", 0)
            limit = response.headers.get("X-RateLimit-Limit", 0)
            if response.status_code == 200:
                self.log.info(
                    "{} Get {} {}s limit: {}/{} {} {} ".format(
                        self.name,
                        url,
                        speed_time,
                        r_limit,
                        limit,
                        args_str,
                        response.status_code,
                    )
                )
                return response
            else:
                self.log.info(
                    "{} Get {} limit: {}/{} {} {} {}s ERROR: {}.".format(
                        self.name,
                        url,
                        r_limit,
                        limit,
                        args_str,
                        response.status_code,
                        speed_time,
                        response.content,
                    )
                )
                return None
        except Exception as e:
            self.log.exception(e)
            self.log.error("Get {} {} FAIL. {}".format(url, args_str, e))
            return None

    def _start(self):
        pass

    def start(self):
        try:
            s_time = time.time()
            self._start()
            e_time = time.time()
            self.log.info(
                "{} fetch success speed {}s.".format(
                    self.name, round((e_time - s_time), 2)
                )
            )
        except Exception as e:
            self.log.exception(e)
            self.log.error("{} fetch error. {}".format(self.name, e))
