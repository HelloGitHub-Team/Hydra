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
    _data = json.load(f)


def test_wechat(requests_mock: Any) -> None:
    article_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    requests_mock.post(article_url, json=_data)
    wechat_result = WeChat().start()
    assert wechat_result is True


def test_wechat_fail(requests_mock: Any) -> None:
    article_url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    requests_mock.post(article_url, json={"success": False})
    wechat_result = WeChat().start()
    assert wechat_result is False
