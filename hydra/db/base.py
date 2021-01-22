#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-14 22:56
#   Desc    :
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

from hydra.config import Config

engine = create_engine(
    Config.database_url(), pool_pre_ping=True, encoding="utf8", echo=False
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 自定义输出实例化对象时的信息
    def __repr__(self) -> str:
        return "custom: < meta data({})>".format(self.__dict__)

    def to_dict(self) -> dict:
        return {c: getattr(self, c) for c in self.__dict__ if not c.startswith("_")}


@contextmanager
def get_db() -> Generator:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
