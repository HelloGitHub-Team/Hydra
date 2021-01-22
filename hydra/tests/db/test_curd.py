#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-15 00:02
#   Desc    :   数据库增删改差测试
from typing import Generator

import pytest
from sqlalchemy.orm import Session

from hydra.db.base import get_db
from hydra.db.curd import upinsert_article
from hydra.db.model import Data
from hydra.tests.utils import utils

SUMMARY = "Python 无敌！"

_data = {
    "content_type": utils.random_bigint(),
    "platform": utils.random_bigint(),
    "source_id": str(utils.random_int(1000)),
    "clicks_count": utils.random_bigint(5),
    "share_count": utils.random_bigint(2),
    "is_original": utils.random_int(),
    "summary": utils.random_gbk2312(),
    "url": utils.random_url(),
    "public_time": utils.random_datetime_str(),
    "update_time": utils.random_datetime_str(),
    "get_time": utils.random_datetime_str(),
}


@pytest.fixture(scope="module")
def db() -> Generator:
    with get_db() as db:
        yield db


def test_upinsert_data(db: Session) -> None:
    data = upinsert_article(db, _data)
    assert data.content_type == _data["content_type"]
    assert data.platform == _data["platform"]
    assert data.source_id == _data["source_id"]
    assert data.summary == _data["summary"]
    assert data.source_id == _data["source_id"]
    assert data.clicks_count == _data["clicks_count"]
    assert data.is_original == _data["is_original"]
    assert data.summary == _data["summary"]
    assert data.url == _data["url"]
    assert data.update_time.strftime(utils.DATE_FORMAT) == _data["update_time"]
    assert data.get_time.strftime(utils.DATE_FORMAT) == _data["get_time"]
    _data["summary"] = SUMMARY
    article = upinsert_article(db, _data)
    assert article.summary == _data["summary"]


def test_query(db: Session) -> None:
    result = db.query(Data).filter_by().first()
    print(result)
    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)


def test_delete_data(db: Session) -> None:
    del_result = db.query(Data).filter_by(url=_data["url"]).delete()
    assert del_result >= 1
