#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-22 15:36
#   Desc    :   CSDN
import datetime

from requests_html import HTML

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


class Csdn(BaseSpider):
    def __init__(self) -> None:
        super(Csdn, self).__init__()
        self.platform = "csdn"
        self.user_id = "a419240016"

    def get_articles(self) -> None:
        url = "https://blog.csdn.net/community/home-api/v1/get-business-list"
        articles = []
        params = {
            "page": 1,
            "size": 20,
            "businessType": "blog",
            "noMore": "false",
            "username": self.user_id,
        }
        rs = self.request_data(url=url, params=params)
        if rs:
            json_data = rs.json()
            articles = json_data.get("data", {}).get("list", [])
            if not articles:
                return
        for article in articles:
            publish_time = datetime.datetime.strptime(
                article["postTime"], "%Y-%m-%d %H:%M:%S"
            )
            article_type = int(article.get("type", 0))
            if article_type == 1:
                is_original = 1
            else:
                is_original = 0
            self.content_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": article["articleId"],
                    "is_original": is_original,
                    "like_count": article["diggCount"],
                    "clicks_count": article["viewCount"],
                    "comment_count": article["commentCount"],
                    "summary": article["title"],
                    "url": article["url"],
                    "publish_time": publish_time,
                    "publish_date": publish_time.date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(articles)} article data finish.")

    def get_account_info(self) -> None:
        """
        获取账户数据
        """
        url = f"https://blog.csdn.net/{self.user_id}"
        rs = self.request_data(url=url, params={"type": "blog"})
        if rs is None:
            return
        html = HTML(html=rs.text)
        rank = int(
            html.xpath('//div[@class="user-profile-head-info-b"]' "/ul/li/a/div")[
                2
            ].text.replace(",", "")
        )
        fans = int(
            html.xpath('//div[@class="user-profile-head-info-b"]' "/ul/li/a/div")[
                4
            ].text.replace(",", "")
        )
        self.account_result = {
            "platform": self.platform,
            "fans": fans,
            "rank": rank,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        self.log.info(f"Download {self.platform} account data finish.")

    def _start(self) -> None:
        self.get_articles()
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
