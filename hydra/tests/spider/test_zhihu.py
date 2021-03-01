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

from hydra.spider.zhihu import Zhihu

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/zhihu_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/zhihu_pin.json"
with open(data_file, "r") as f:
    pin_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/zhihu_account.json"
with open(data_file, "r") as f:
    account_data = json.load(f)


def test_zhihu_fail(requests_mock: Any) -> None:
    article_url = "https://www.zhihu.com/api/v4/creators/creations/article"
    pin_url = "https://www.zhihu.com/api/v4/creators/creations/pin"
    fans_url = "https://www.zhihu.com/api/v4/creators/homepage"
    requests_mock.get(article_url, json={"data": None})
    requests_mock.get(pin_url, json={"data": None})
    requests_mock.get(fans_url, json={})
    Zhihu().start()


def test_zhihu(requests_mock: Any) -> None:
    article_url = "https://www.zhihu.com/api/v4/creators/creations/article"
    pin_url = "https://www.zhihu.com/api/v4/creators/creations/pin"
    fans_url = "https://www.zhihu.com/api/v4/creators/homepage"
    requests_mock.get(article_url, json=article_data)
    requests_mock.get(pin_url, json=pin_data)
    requests_mock.get(fans_url, json=account_data)
    Zhihu().start()
