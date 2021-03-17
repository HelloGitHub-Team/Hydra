#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-22 15:24
#   Desc    :   运行
import time

import schedule
import sentry_sdk

from hydra.spider import *
from hydra.config import Config, logger

sentry_config = Config.sentry_config()
sentry_sdk.init(**sentry_config)

SPIDER_LIST = [WeChat, Cnblogs, Toutiao, Csdn, Zhihu, Juejin, Jike]


def job():
    for spider in SPIDER_LIST:
        spider().start()


schedule.every().day.at("06:30").do(job)
schedule.every().day.at("11:30").do(job)
schedule.every().day.at("18:30").do(job)
schedule.every().day.at("21:00").do(job)

logger.info("Start running job...")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    logger.error(f"Running schedule error: {e}")
