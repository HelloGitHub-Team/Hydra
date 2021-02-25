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

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/toutiao_micro.json"
with open(data_file, "r") as f:
    micro_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/toutiao_fans.json"
with open(data_file, "r") as f:
    fans_data = json.load(f)


def test_toutiao_fail(requests_mock: Any) -> None:
    article_url = "https://www.toutiao.com/api/pc/feed/?category=pc_profile_article"
    micro_url = "https://www.toutiao.com/api/pc/feed/?category=pc_profile_ugc"
    fans_url = "https://www.toutiao.com/api/pc/user/fans_stat"
    requests_mock.get(article_url, json={"message": "fail"})
    requests_mock.get(micro_url, json={"message": "fail"})
    requests_mock.post(fans_url, json={"message": "fail"})
    Toutiao().start()


def test_toutiao(requests_mock: Any) -> None:
    article_url = "https://www.toutiao.com/api/pc/feed/?category=pc_profile_article"
    micro_url = "https://www.toutiao.com/api/pc/feed/?category=pc_profile_ugc"
    fans_url = "https://www.toutiao.com/api/pc/user/fans_stat"
    requests_mock.get(article_url, json=article_data)
    requests_mock.get(micro_url, json=micro_data)
    requests_mock.post(fans_url, json=fans_data)
    Toutiao().start()
