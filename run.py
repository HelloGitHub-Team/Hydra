#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-22 15:24
#   Desc    :   运行
import time

import schedule

from hydra.spider import *

SPIDER_MAP = {
    "wechat": WeChat(), "cnblogs": Cnblogs(), "toutiao": Toutiao(),
    "csdn": Csdn(), "zhihu": Zhihu(), "juejin": Juejin(), "jike": Jike()
}


def job():
    for spider in SPIDER_MAP.values():
        spider.start()


schedule.every().day.at("06:30").do(job)
schedule.every().day.at("11:30").do(job)
schedule.every().day.at("21:00").do(job)

print("Start running job...")

while True:
    schedule.run_pending()
    time.sleep(1)
