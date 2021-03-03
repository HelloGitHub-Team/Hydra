#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 18:36
#   Desc    :
import json
import os
from typing import Any

from hydra.spider.toutiao import Toutiao

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/toutiao_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/toutiao_pin.json"
with open(data_file, "r") as f:
    pin_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/toutiao_fans.json"
with open(data_file, "r") as f:
    fans_data = json.load(f)

article_url = (
    "https://mp.toutiao.com/mp/agw/statistic/v2/item/list?type=1&"
    "page_size=30&page_num=1&app_id=1231"
)
pin_url = (
    "https://mp.toutiao.com/mp/agw/statistic/v2/item/list?type=3&"
    "page_size=30&page_num=1&app_id=1231"
)
fans_url = "https://mp.toutiao.com/mp/agw/statistic/v2/fans/latest_stat?app_id=1231"


def test_toutiao_fail(requests_mock: Any) -> None:
    requests_mock.get(article_url, json={"message": "fail"})
    requests_mock.get(pin_url, json={"message": "fail"})
    requests_mock.get(fans_url, json={"message": "fail"})
    Toutiao().start()


def test_toutiao(requests_mock: Any) -> None:
    requests_mock.get(article_url, json=article_data)
    requests_mock.get(pin_url, json=pin_data)
    requests_mock.get(fans_url, json=fans_data)
    Toutiao().start()
