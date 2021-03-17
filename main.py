#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-22 15:24
#   Desc    :   运行
import argparse

from hydra.spider import *

SPIDER_MAP = {
    "wechat": WeChat, "cnblogs": Cnblogs, "toutiao": Toutiao,
    "csdn": Csdn, "zhihu": Zhihu, "juejin": Juejin, "jike": Jike
}


if __name__ == "__main__":
    # 1. 设置解析器
    parser = argparse.ArgumentParser(description='Script run')
    # 2. 定义参数
    parser.add_argument('name', metavar='name', type=str)
    # 3. 解析命令行
    args = parser.parse_args()
    name = args.name

    spider = SPIDER_MAP.get(name)
    if spider:
        spider().start()
    elif name == "all":
        for fi_spider in SPIDER_MAP.values():
            fi_spider().start()
    else:
        print("spider name error.")
