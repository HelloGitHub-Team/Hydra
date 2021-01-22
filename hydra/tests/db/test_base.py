#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 19:52
#   Desc    :
from hydra.db.base import get_db


def test_error() -> None:
    try:
        with get_db() as db:
            db.query1()
    except AttributeError:
        pass
