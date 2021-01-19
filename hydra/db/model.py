#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-12 21:26
#   Desc    :
import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, String

from hydra.db.base import Base, engine


class Article(Base):
    __tablename__ = "hydra_article"

    url = Column(String(255))  # 文章地址
    title = Column(String(255))  # 标题
    is_original = Column(Integer, default=0)  # 是否为原创：1 为原创
    is_head = Column(Integer, default=0)  # 是否为头条：1 为头条
    clicks_count = Column(Integer)  # 阅读数
    collect_count = Column(Integer)  # 收藏数
    share_count = Column(Integer)  # 分享数
    like_count = Column(Integer)  # 喜欢数
    comment_count = Column(Integer)  # 评论数
    source_id = Column(Integer)  # 来源 ID

    public_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 文章发布时间
    update_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 数据源更新时间
    get_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 获取到数据的时间


Base.metadata.create_all(engine)
