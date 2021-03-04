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

from hydra.spider.csdn import Csdn

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/csdn.txt"
with open(data_file, "r") as f:
    html_data = f.read()

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/csdn_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

url = "https://blog.csdn.net/a419240016"
article_url = (
    "https://blog.csdn.net/community/home-api/v1/get-business-list?"
    "page=1&size=20&businessType=blog&noMore=false&username=a419240016"
)


def test_csdn_fail(requests_mock: Any) -> None:
    requests_mock.get(url, status_code=404)
    requests_mock.get(article_url, json={})
    Csdn().start()


def test_csdn(requests_mock: Any) -> None:
    requests_mock.get(url, text=html_data)
    requests_mock.get(article_url, json=article_data)
    Csdn().start()
