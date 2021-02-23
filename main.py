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


if __name__ == "__main__":
    # 1. 设置解析器
    parser = argparse.ArgumentParser(description='Script run')
    # 2. 定义参数
    parser.add_argument('name',  metavar='name', type=str)
    # 3. 解析命令行
    args = parser.parse_args()
    name = args.name

    if name == 'wechat':
        w = WeChat()
        w.start()
    elif name == 'cnblogs':
        c = Cnblogs()
        c.start()
