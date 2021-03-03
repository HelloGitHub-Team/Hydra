#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-23 22:04
#   Desc    :   今日头条
import datetime

from hydra.config import Config
from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


"""
https://www.toutiao.com/c/user/61302299383/
"""


class Toutiao(BaseSpider):
    def __init__(self) -> None:
        super(Toutiao, self).__init__()
        self.platform = "toutiao"
        self.cookie = Config.toutiao()

    @staticmethod
    def make_url(request_type: str) -> str:
        if request_type == "article":
            flag = 1
        else:
            flag = 3
        url = (
            f"https://mp.toutiao.com/mp/agw/statistic/v2/item/list?"
            f"type={flag}&page_size=30&page_num=1&app_id=1231"
        )
        return url

    def get_articles(self) -> None:
        """
        获取文章数据
        """
        rs = self.request_data(url=self.make_url("article"), cookies=self.cookie)
        json_data = dict()
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return
        data = json_data.get("item_datas", [])
        for item in data:
            interaction_data = item["item_stat"]["interaction_data"]
            # 分享=转发+分享
            share_count = (
                interaction_data["share_count"] + interaction_data["forward_count"]
            )
            source_id = item["item_id"]
            publish_datetime = datetime.datetime.fromtimestamp(item["create_time"])
            self.content_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": source_id,
                    "clicks_count": item["item_stat"]["consume_data"][
                        "go_detail_count"
                    ],
                    "like_count": interaction_data["digg_count"],
                    "comment_count": interaction_data["comment_count"],
                    "share_count": share_count,
                    "collect_count": interaction_data["repin_count"],
                    "summary": item["title"],
                    "url": f"https://www.toutiao.com/item/{source_id}/",
                    "publish_time": publish_datetime,
                    "publish_date": publish_datetime.date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(data)} article data finish.")

    def get_pins(self) -> None:
        """
        获取微头条数据
        """
        rs = self.request_data(url=self.make_url("pin"), cookies=self.cookie)
        json_data = {}
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return
        data = json_data.get("item_datas", [])
        for item in data:
            publish_datetime = datetime.datetime.fromtimestamp(item["create_time"])
            source_id = item["item_id"]
            summary = item["title"][:50].strip()
            interaction_data = item["item_stat"]["interaction_data"]
            # 分享=转发+分享
            share_count = (
                interaction_data["share_count"] + interaction_data["forward_count"]
            )
            self.content_result.append(
                {
                    "content_type": "pin",
                    "platform": self.platform,
                    "source_id": source_id,
                    "clicks_count": item["item_stat"]["consume_data"][
                        "go_detail_count"
                    ],
                    "like_count": interaction_data["digg_count"],
                    "comment_count": interaction_data["comment_count"],
                    "share_count": share_count,
                    "collect_count": interaction_data["repin_count"],
                    "summary": summary,
                    "url": f"https://www.toutiao.com/w/a{source_id}/",
                    "publish_time": publish_datetime,
                    "publish_date": publish_datetime.date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(data)} pin data finish.")

    def get_account_info(self) -> None:
        url = "https://mp.toutiao.com/mp/agw/statistic/v2/fans/latest_stat?app_id=1231"
        json_data = {}
        rs = self.request_data(url=url, cookies=self.cookie)
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return
        self.account_result = {
            "platform": self.platform,
            "fans": -1,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        fans = json_data.get("fans_stat", {}).get("total_fans_count", -1)
        self.account_result["fans"] = fans
        self.log.info(f"Download {self.platform} account data finish.")

    def _start(self) -> None:
        self.get_articles()
        self.get_pins()
        self.get_account_info()
        if not self.result_is_empty():
            with get_db() as db:
                insert_account(db, self.account_result)
                for item in self.content_result:
                    upinsert_content(db, item)
        self.log.info(
            f"Save {self.name} content: {len(self.content_result)} "
            f"| account: {self.account_result} data finish."
        )
