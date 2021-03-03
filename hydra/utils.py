#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 16:00
#   Desc    :
import os
from http.cookies import SimpleCookie
from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger
from logging.handlers import (
    BaseRotatingHandler,
    RotatingFileHandler,
    TimedRotatingFileHandler,
)


def init_log(name: str, log_type: str = None) -> Logger:
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs/")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    handler: BaseRotatingHandler = RotatingFileHandler(
        os.path.join(log_path, "{}.log".format(name)), encoding="utf-8"
    )
    if log_type == "time":
        handler = TimedRotatingFileHandler(
            os.path.join(log_path, "{}.log".format(name)),
            when="midnight",
            backupCount=10,
            encoding="utf-8",
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


def make_cookie(cookie_str: str) -> dict:
    cookie_dict = {}
    cookie: SimpleCookie = SimpleCookie()
    cookie.load(cookie_str)
    for k, v in cookie.items():
        cookie_dict[k] = v.value
    return cookie_dict
