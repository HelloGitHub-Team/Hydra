#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-28 23:33
#   Desc    :   知乎
import datetime

from hydra.config import Config
from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


class Zhihu(BaseSpider):
    def __init__(self) -> None:
        super(Zhihu, self).__init__()
        self.platform = "zhihu"
        self.headers = {"content-type": "application/json"}
        self.cookie = Config.zhihu()

    def get_articles(self) -> None:
        """
        获取文章数据
        """
        url = "https://www.zhihu.com/api/v4/creators/creations/article"
        articles = []
        rs = self.request_data(url=url, cookies=self.cookie)
        if rs:
            json_data = rs.json()
            articles = json_data.get("data", [])
            if not articles:
                return
        for article in articles:
            article_data = article["data"]
            article_reaction = article["reaction"]
            source_id = article_data["id"]
            publish_time = datetime.datetime.fromtimestamp(article_data["created_time"])
            self.content_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": source_id,
                    "like_count": article_reaction["vote_up_count"],
                    "clicks_count": article_reaction["read_count"],
                    "comment_count": article_reaction["comment_count"],
                    "collect_count": article_reaction["collect_count"],
                    "summary": article_data["title"],
                    "url": f"https://zhuanlan.zhihu.com/p/{source_id}",
                    "publish_time": publish_time,
                    "publish_date": publish_time.date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(articles)} article data finish.")

    def get_pins(self) -> None:
        """
        获取想法的数据
        """
        url = "https://www.zhihu.com/api/v4/creators/creations/pin"
        pin_list = []
        rs = self.request_data(url=url, cookies=self.cookie)
        if rs:
            json_data = rs.json()
            pin_list = json_data.get("data", [])
            if not pin_list:
                return
        for pin in pin_list:
            pin_data = pin["data"]
            pin_reaction = pin["reaction"]
            source_id = pin_data["id"]
            publish_time = datetime.datetime.fromtimestamp(pin_data["created_time"])
            self.content_result.append(
                {
                    "content_type": "pin",
                    "platform": self.platform,
                    "source_id": source_id,
                    "like_count": pin_reaction["reaction_count"],
                    "clicks_count": pin_reaction["view_count"],
                    "comment_count": pin_reaction["comment_count"],
                    "share_count": pin_reaction["repin_count"],
                    "summary": pin_data["content"][0]["content"][:50].strip(),
                    "url": f"https://www.zhihu.com/pin/{source_id}",
                    "publish_time": publish_time,
                    "publish_date": publish_time.date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(pin_list)} pin data finish.")

    def get_account_info(self) -> None:
        url = "https://www.zhihu.com/api/v4/creators/homepage"
        json_data = {}
        rs = self.request_data(url=url, cookies=self.cookie)
        if rs:
            json_data = rs.json()
            if not json_data:
                return
        self.account_result = {
            "platform": self.platform,
            "fans": json_data.get("statistics", {}).get("total_follower_count", -1),
            "value": json_data.get("level", {}).get("score", -1),
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        self.log.info(f"Download {self.platform} account data finish.")

    def _start(self) -> None:
        self.get_articles()
        self.get_pins()
        self.get_account_info()
        if not self.result_is_empty():
            with get_db() as db:
                insert_account(db, self.account_result)
                for article in self.content_result:
                    upinsert_content(db, article)
        self.log.info(
            f"Save {self.name} content: {len(self.content_result)} "
            f"| account: {self.account_result} data finish."
        )
