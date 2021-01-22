#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 17:18
#   Desc    :
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from hydra.utils import init_log


def test_log() -> None:
    default_log = init_log("test")
    default_success = False
    for handle in default_log.handlers:
        if isinstance(handle, RotatingFileHandler):
            default_success = True
    assert default_success is True
    time_log = init_log("test", "time")
    time_success = False
    for handle in time_log.handlers:
        if isinstance(handle, TimedRotatingFileHandler):
            time_success = True
    assert time_success is True
