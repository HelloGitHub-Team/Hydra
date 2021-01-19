#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-14 23:11
#   Desc    :   操作数据库
from sqlalchemy.orm import Session

from hydra.db.model import Article


def upinsert_article(db: Session, kwargs: dict):
    article = db.query(Article).filter_by(url=kwargs["url"]).first()
    if article:
        db.query(Article).filter_by(url=kwargs["url"]).update(kwargs)
    else:
        article = Article(**kwargs)
        db.add(article)
    db.commit()
    return article
