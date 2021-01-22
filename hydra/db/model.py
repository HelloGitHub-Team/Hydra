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


class Data(Base):
    __tablename__ = "hydra_data"

    url = Column(String(255))  # 内容地址
    summary = Column(String(255))  # 标题 or 短内容 or 描述（统称为摘要）
    is_original = Column(Integer, default=0)  # 是否为原创：1 为原创
    is_head = Column(Integer, default=0)  # 是否为头条：1 为头条
    clicks_count = Column(Integer)  # 阅读数
    collect_count = Column(Integer)  # 收藏数
    share_count = Column(Integer)  # 分享数
    like_count = Column(Integer)  # 喜欢数
    comment_count = Column(Integer)  # 评论数
    source_id = Column(String(255))  # 对应平台上的唯一 ID
    platform = Column(Integer)  # 平台 ID
    content_type = Column(Integer)  # 内容类别：文章、微内容、视频

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
