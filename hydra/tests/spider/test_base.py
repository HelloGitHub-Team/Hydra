#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 18:34
#   Desc    :
import datetime
from typing import Any

from hydra.spider.base import BaseSpider


def test_base(requests_mock: Any) -> None:
    requests_mock.get("https://test.com", status_code=500)
    bs = BaseSpider()
    assert bs.get_date == datetime.date.today().strftime("%Y-%m-%d")
    bs.request_data(url="https://test.com", auth={})
    bs.start()
    bs.request_data(url="test.com", auth={})
