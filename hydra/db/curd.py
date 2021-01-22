#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-14 23:11
#   Desc    :   操作数据库
from sqlalchemy.orm import Session

from hydra.db.model import Account, Content


def upinsert_content(db: Session, kwargs: dict) -> Content:
    content = db.query(Content).filter_by(source_id=kwargs["source_id"]).first()
    if content:
        db.query(Content).filter_by(source_id=kwargs["source_id"]).update(kwargs)
    else:
        content = Content(**kwargs)
        db.add(content)
    db.commit()
    return content


def insert_account(db: Session, kwargs: dict) -> Account:
    account = (
        db.query(Account)
        .filter_by(platform=kwargs["platform"], update_date=kwargs["update_date"])
        .first()
    )
    if not account:
        account = Account(**kwargs)
        db.add(account)
    db.commit()
    return account
