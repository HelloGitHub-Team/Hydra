#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 18:36
#   Desc    :
import os
from typing import Any

from hydra.spider.csdn import Csdn

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/csdn.txt"
with open(data_file, "r") as f:
    html_data = f.read()


def test_csdn_fail(requests_mock: Any) -> None:
    url = "https://blog.csdn.net/a419240016"
    requests_mock.get(url, status_code=404)
    Csdn().start()


def test_cnblogs(requests_mock: Any) -> None:
    url = "https://blog.csdn.net/a419240016"
    requests_mock.get(url, text=html_data)
    Csdn().start()
