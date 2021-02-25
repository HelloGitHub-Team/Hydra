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

from hydra.spider.wechat import WeChat

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/wechat_article.json"
with open(data_file, "r") as f:
    article_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/wechat_rank.json"
with open(data_file, "r") as f:
    rank_data = json.load(f)

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/wechat_fans.json"
with open(data_file, "r") as f:
    fans_data = json.load(f)


def test_wechat_fail(requests_mock: Any) -> None:
    article_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    rank_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/data/rankings"
    fans_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/head/getEstimateFansNum"
    requests_mock.post(article_url, json={"success": False})
    requests_mock.post(rank_url, json={"success": False})
    requests_mock.post(fans_url, json={"success": False})
    WeChat().start()


def test_wechat_fail2(requests_mock: Any) -> None:
    article_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    requests_mock.post(article_url, status_code=404)
    WeChat().start()


def test_wechat(requests_mock: Any) -> None:
    article_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    rank_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/data/rankings"
    fans_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/head/getEstimateFansNum"
    requests_mock.post(article_url, json=article_data)
    requests_mock.post(rank_url, json=rank_data)
    requests_mock.post(fans_url, json=fans_data)
    WeChat().start()
