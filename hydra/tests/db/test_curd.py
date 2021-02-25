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
from hydra.db.curd import insert_account, upinsert_content
from hydra.db.model import Content
from hydra.tests.utils import utils

SUMMARY = "Python 无敌！"

content_data = {
    "content_type": utils.random_lower_string(),
    "platform": utils.random_lower_string(10),
    "source_id": str(utils.random_int(1000)),
    "clicks_count": utils.random_bigint(5),
    "share_count": utils.random_bigint(2),
    "is_original": utils.random_int(),
    "summary": utils.random_gbk2312(),
    "url": utils.random_url(),
    "publish_time": utils.random_datetime_str(),
    "publish_date": utils.random_date_str(),
    "update_time": utils.random_datetime_str(),
    "get_time": utils.random_datetime_str(),
}

account_data = {
    "platform": utils.random_lower_string(4),
    "fans": utils.random_bigint(5),
    "rank": utils.random_bigint(3),
    "value": utils.random_float(3),
    "update_date": utils.random_date_str(),
    "get_time": utils.random_datetime_str(),
}


@pytest.fixture(scope="module")
def db() -> Generator:
    with get_db() as db:
        yield db


def test_upinsert_content(db: Session) -> None:
    data = upinsert_content(db, content_data)
    assert data.content_type == content_data["content_type"]
    assert data.platform == content_data["platform"]
    assert data.source_id == content_data["source_id"]
    assert data.summary == content_data["summary"]
    assert data.clicks_count == content_data["clicks_count"]
    assert data.is_original == content_data["is_original"]
    assert data.summary == content_data["summary"]
    assert data.url == content_data["url"]
    assert data.update_time.strftime(utils.TIME_FORMAT) == content_data["update_time"]
    assert data.get_time.strftime(utils.TIME_FORMAT) == content_data["get_time"]
    content_data["summary"] = SUMMARY
    article = upinsert_content(db, content_data)
    assert article.summary == content_data["summary"]


def test_query(db: Session) -> None:
    result = db.query(Content).filter_by().first()
    print(result)
    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)


def test_delete_data(db: Session) -> None:
    del_result = db.query(Content).filter_by(url=content_data["url"]).delete()
    assert del_result >= 1


def test_insert_account(db: Session) -> None:
    account = insert_account(db, account_data)
    assert account.fans == account_data["fans"]
    insert_account(db, account_data)
