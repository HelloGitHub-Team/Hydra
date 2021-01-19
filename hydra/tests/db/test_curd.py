#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-15 00:02
#   Desc    :   数据库增删改差测试
from sqlalchemy.orm import Session

from hydra.db.base import get_db
from hydra.db.curd import upinsert_article
from hydra.db.model import Article
from hydra.tests.utils import utils

TITLE = "Python 无敌！"

_data = {
    "source_id": utils.random_int(1000),
    "clicks_count": utils.random_bigint(5),
    "share_count": utils.random_bigint(2),
    "is_original": utils.random_int(),
    "public_time": utils.random_datetime_str(),
    "title": utils.random_gbk2312(),
    "url": utils.random_url(),
    "update_time": utils.random_datetime_str(),
    "get_time": utils.random_datetime_str(),
}


def test_error() -> None:
    try:
        with get_db() as db:
            db.query1()
    except AttributeError:
        pass


def test_upinsert_article(db: Session) -> None:
    article = upinsert_article(db, _data)
    assert article.title == _data["title"]
    assert article.source_id == _data["source_id"]
    assert article.clicks_count == _data["clicks_count"]
    assert article.is_original == _data["is_original"]
    assert article.title == _data["title"]
    assert article.url == _data["url"]
    assert article.update_time.strftime(utils.DATE_FORMAT) == _data["update_time"]
    assert article.get_time.strftime(utils.DATE_FORMAT) == _data["get_time"]
    _data["title"] = TITLE
    article = upinsert_article(db, _data)
    assert article.title == _data["title"]


def test_query(db: Session) -> None:
    result = db.query(Article).filter_by().first()
    print(result)
    result_dict = result.to_dict()
    assert isinstance(result_dict, dict)


def test_delete_aritcle(db: Session) -> None:
    del_result = db.query(Article).filter_by(url=_data["url"]).delete()
    assert del_result == 1
