#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-12 21:26
#   Desc    :
import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Date, DateTime, Float, Integer, String

from hydra.db.base import Base, engine


class Content(Base):
    """
    内容数据
    """

    __tablename__ = "hydra_content"

    url = Column(String(255))  # 内容地址
    summary = Column(String(255))  # 标题 or 短内容 or 描述（统称为摘要）
    is_original = Column(Integer)  # 是否为原创：1 为原创
    is_head = Column(Integer)  # 是否为头条：1 为头条
    clicks_count = Column(Integer)  # 阅读数
    collect_count = Column(Integer)  # 收藏数
    share_count = Column(Integer)  # 分享数
    like_count = Column(Integer)  # 喜欢数
    comment_count = Column(Integer)  # 评论数
    source_id = Column(String(255))  # 对应平台上内容的唯一 ID
    platform = Column(String(255))  # 平台名称
    content_type = Column(String(255))  # 内容类别：文章(article)、微内容(micro)、视频(video)

    publish_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 内容发布时间
    publish_date = Column(
        Date, default=datetime.datetime.now().strftime("%Y-%m-%d")
    )  # 内容发布日期
    update_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 数据源更新时间
    get_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 获取到数据的时间


class Account(Base):
    """
    账号数据
    """

    __tablename__ = "hydra_account"

    platform = Column(String(255))  # 平台名称
    fans = Column(Integer)  # 粉丝数
    rank = Column(Integer)  # 排名
    value = Column(Float)  # 平台的分数

    update_date = Column(
        Date, default=datetime.datetime.now().strftime("%Y-%m-%d")
    )  # 数据源更新日期
    get_time = Column(
        DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # 获取到数据的时间


Base.metadata.create_all(engine)
