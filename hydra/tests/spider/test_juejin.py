#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XiaoBei
#   E-mail  :   529352969@qq.com
#   Date    :   2021-02-26 18:44
#   Desc    :
import json
import os
from typing import Any

from hydra.spider.juejin import Juejin

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/juejin_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/juejin_pin.json"
with open(data_file, "r") as f:
    pin_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/juejin_fans.json"
with open(data_file, "r") as f:
    fans_data = json.load(f)


def test_juejin_fail(requests_mock: Any) -> None:
    article_url = "https://api.juejin.cn/content_api/v1/article/query_list"
    fans_url = "https://api.juejin.cn/user_api/v1/user/get"
    pin_url = "https://api.juejin.cn/content_api/v1/short_msg/query_list"
    requests_mock.post(article_url, json={"err_msg": "fail"})
    requests_mock.post(pin_url, json={"err_msg": "fail"})
    requests_mock.get(fans_url, json={"err_msg": "fail"})
    Juejin().start()


def test_juejin(requests_mock: Any) -> None:
    article_url = "https://api.juejin.cn/content_api/v1/article/query_list"
    fans_url = "https://api.juejin.cn/user_api/v1/user/get"
    pin_url = "https://api.juejin.cn/content_api/v1/short_msg/query_list"
    requests_mock.post(article_url, json=article_data)
    requests_mock.post(pin_url, json=pin_data)
    requests_mock.get(fans_url, json=fans_data)
    Juejin().start()
