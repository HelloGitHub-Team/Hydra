#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-22 15:24
#   Desc    :
import argparse

from hydra.spider.wechat import WeChat
from hydra.spider.cnblogs import Cnblogs
from hydra.spider.toutiao import Toutiao
from hydra.spider.csdn import Csdn
from hydra.spider.zhihu import Zhihu

if __name__ == "__main__":
    # 1. 设置解析器
    parser = argparse.ArgumentParser(description='Script run')
    # 2. 定义参数
    parser.add_argument('name', metavar='name', type=str)
    # 3. 解析命令行
    args = parser.parse_args()
    name = args.name
    spider_map = {
        "wechat": WeChat(), "cnblogs": Cnblogs(), "toutiao": Toutiao(),
        "csdn": Csdn(), "zhihu": Zhihu()}

    spider = spider_map.get(name)
    if spider:
        spider.start()
