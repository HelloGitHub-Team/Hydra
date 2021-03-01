#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XiaoBei
#   E-mail  :   529352969@qq.com
#   Date    :   2021-02-26 14:20
#   Desc    :   掘金
import datetime
import json
import os
from typing import Any, Dict, List

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider
from datetime import datetime

"""
url: https://api.juejin.cn/content_api/v1/article/query_list
params: {
            "user_id": "1574156384091320",
            "sort_type": 2,
            "cursor": "50"
        }
"""


class Juejin(BaseSpider):
    def __init__(self) -> None:
        super(Juejin, self).__init__()
        self.platform = "juejin"
        self.site = "https://juejin.cn/"
        self.articles_result: List[Dict[str, Any]] = []
        self.hotspot_result: List[Dict[str, Any]] = []
        self.cursor = 0

    def get_articles_list(self) -> list:
        """
        获取文章数据
        """
        json_data = dict()
        url = "https://api.juejin.cn/content_api/v1/article/query_list"
        payload = {"user_id": "1574156384091320", "sort_type": 2, "cursor": str(self.cursor)}
        headers = {
            'Content-Type': 'application/json'
        }
        rs = self.request_data(
            'POST',
            url=url,
            data=json.dumps(payload),
            headers=headers
        )
        if rs:
            json_data = rs.json()
            if json_data["err_msg"] != "success" or not json_data['data']:
                return self.articles_result

            for article in json_data["data"]:
                self.articles_result.append(
                    {
                        "content_type": "article",
                        "platform": self.platform,
                        "source_id": article['article_id'],
                        "clicks_count": article['article_info']['view_count'],
                        "like_count": article['article_info']['digg_count'],
                        "comment_count": article['article_info']['comment_count'],
                        "summary": article['article_info']['title'],
                        "url": self.site + 'post/' + str(article['article_id']),
                        "is_original": article['article_info']['is_original'],
                        "is_head": article['article_info']['is_hot'],
                        "publish_time": datetime.fromtimestamp(int(article['article_info']['ctime'])),
                        "publish_date": datetime.fromtimestamp(int(article['article_info']['ctime'])).date(),
                        "get_time": self.get_time,
                        "update_time": self.get_time,
                    }
                )
            if json_data['has_more']:
                self.cursor += 10
                self.get_articles_list()

            self.cursor = 0

        return self.articles_result

    def get_account_info(self) -> dict:
        json_data = {}
        account_result: Dict[str, Any] = {
            "platform": self.platform,
            "fans": -1,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        url = "https://api.juejin.cn/user_api/v1/user/get?aid=2608&user_id=1574156384091320&not_self=1"
        rs = self.request_data(
            url=url
        )
        if rs:
            json_data = rs.json()
            if json_data["err_msg"] != "success":
                return account_result
        fans = str(json_data.get("data", {}).get("follower_count", "-1"))
        if fans.count("万") > 0:
            fans = int(float(fans.replace("万", "")) * 10000)
        account_result["fans"] = fans
        account_result["value"] = json_data.get("data", {}).get("power", "-1")
        self.log.info(f"Download {self.platform} account data finish.")
        return account_result

    def get_hotspot_list(self) -> list:
        """
        获取沸点数据
        """
        url = "https://api.juejin.cn/content_api/v1/short_msg/query_list"
        payload = {'sort_type': 4, 'cursor': str(self.cursor), 'limit': 20, 'user_id': "1574156384091320"}
        headers = {
            'Content-Type': 'application/json'
        }
        hotspot_result: List[Dict[str, Any]] = []
        rs = self.request_data(
            'POST',
            url=url,
            data=json.dumps(payload),
            headers=headers
        )
        if rs:
            json_data = rs.json()
            if json_data["err_msg"] != "success" or not json_data['data']:
                return hotspot_result
            for essay in json_data["data"]:
                self.hotspot_result.append(
                    {
                        "content_type": "micro",
                        "platform": self.platform,
                        "source_id": essay['msg_id'],
                        "like_count": essay['msg_Info']['digg_count'],
                        "comment_count": essay['msg_Info']['comment_count'],
                        "summary": essay['msg_Info']['content'][:30],
                        "publish_time": datetime.fromtimestamp(int(essay['msg_Info']['ctime'])),
                        "publish_date": datetime.fromtimestamp(int(essay['msg_Info']['ctime'])).date(),
                        "get_time": self.get_time,
                        "update_time": self.get_time,
                    }
                )
            if json_data['has_more']:
                self.cursor += 20
                self.get_hotspot_list()

            self.cursor = 0

        self.log.info(f"Download {len(self.hotspot_result)} hotspot data finish.")

        return self.hotspot_result

    def _start(self) -> None:
        articles_list = self.get_articles_list()
        hotspot_list = self.get_hotspot_list()
        account_info = self.get_account_info()
        if not articles_list or not account_info or not hotspot_list:
            raise Exception
        with get_db() as db:
            insert_account(db, account_info)
            for article in articles_list:
                upinsert_content(db, article)
            for hotspot in hotspot_list:
                upinsert_content(db, hotspot)

