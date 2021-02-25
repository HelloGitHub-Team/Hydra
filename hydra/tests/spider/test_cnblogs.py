#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 18:36
#   Desc    :
import os
from typing import Any

from hydra.spider.cnblogs import Cnblogs

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/cnblogs_article.txt"
with open(data_file, "r") as f:
    article_data = f.read()

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/cnblogs_rank.txt"
with open(data_file, "r") as f:
    rank_data = f.read()

data_file = os.path.dirname(os.path.dirname(__file__)) + "/data/cnblogs_fans.txt"
with open(data_file, "r") as f:
    fans_data = f.read()


def test_cnblogs_fail(requests_mock: Any) -> None:
    article_url = "https://www.cnblogs.com/xueweihan/"
    rank_url = "https://www.cnblogs.com/xueweihan/ajax/sidecolumn.aspx"
    fans_url = "https://www.cnblogs.com/xueweihan/ajax/news.aspx"
    requests_mock.get(article_url, status_code=404)
    requests_mock.get(rank_url, status_code=404)
    requests_mock.get(fans_url, status_code=404)
    Cnblogs().start()


def test_cnblogs_fail2(requests_mock: Any) -> None:
    article_url = "https://www.cnblogs.com/xueweihan/"
    rank_url = "https://www.cnblogs.com/xueweihan/ajax/sidecolumn.aspx"
    fans_url = "https://www.cnblogs.com/xueweihan/ajax/news.aspx"
    requests_mock.get(article_url, text=article_data)
    requests_mock.get(rank_url, status_code=404)
    requests_mock.get(fans_url, text=fans_data)
    Cnblogs().start()


def test_cnblogs(requests_mock: Any) -> None:
    article_url = "https://www.cnblogs.com/xueweihan/"
    rank_url = "https://www.cnblogs.com/xueweihan/ajax/sidecolumn.aspx"
    fans_url = "https://www.cnblogs.com/xueweihan/ajax/news.aspx"
    requests_mock.get(article_url, text=article_data)
    requests_mock.get(rank_url, text=rank_data)
    requests_mock.get(fans_url, text=fans_data)
    Cnblogs().start()
