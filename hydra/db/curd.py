#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-14 23:11
#   Desc    :   操作数据库
from sqlalchemy.orm import Session

from hydra.db.model import Data


def upinsert_article(db: Session, kwargs: dict) -> Data:
    article = db.query(Data).filter_by(source_id=kwargs["source_id"]).first()
    if article:
        db.query(Data).filter_by(source_id=kwargs["source_id"]).update(kwargs)
    else:
        article = Data(**kwargs)
        db.add(article)
    db.commit()
    return article
