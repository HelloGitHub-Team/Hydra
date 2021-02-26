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

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/junjin_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/junjin_fans.json"
with open(data_file, "r") as f:
    fans_data = json.load(f)


def test_junjin_fail(requests_mock: Any) -> None:
    article_url = "https://api.juejin.cn/content_api/v1/article/query_list"
    fans_url = "https://api.juejin.cn/user_api/v1/user/get?aid=2608&user_id=1574156384091320&not_self=1"
    requests_mock.get(article_url, json={"message": "fail"})
    requests_mock.post(fans_url, json={"message": "fail"})
    Juejin().start()


def test_junjin(requests_mock: Any) -> None:
    article_url = "https://api.juejin.cn/content_api/v1/article/query_list"
    fans_url = "https://api.juejin.cn/user_api/v1/user/get?aid=2608&user_id=1574156384091320&not_self=1"
    requests_mock.get(article_url, json=article_data)
    requests_mock.post(fans_url, json=fans_data)
    Juejin().start()
