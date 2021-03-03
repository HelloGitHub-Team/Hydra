#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 18:36
#   Desc    :
import os
from typing import Any

from hydra.spider.jike import Jike

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/jike.txt"
with open(data_file, "r") as f:
    data = f.read()

url = "https://web.okjike.com/u/ff31a838-6eb9-440d-9970-dabc5b2c0309"


def test_jike_fail(requests_mock: Any) -> None:
    requests_mock.get(url, status_code=404)
    Jike().start()


def test_jike(requests_mock: Any) -> None:
    requests_mock.get(url, text=data)
    Jike().start()
