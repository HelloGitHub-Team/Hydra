#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XiaoBei
#   E-mail  :   529352969@qq.com
#   Date    :   2021-02-26 14:20
#   Desc    :   掘金
import json
from datetime import datetime
from typing import Any, Dict, List

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


"""
url: https://api.juejin.cn/content_api/v1/article/query_list
"""


class Juejin(BaseSpider):
    def __init__(self) -> None:
        super(Juejin, self).__init__()
        self.platform = "juejin"
        self.user_id = "1574156384091320"
        self.headers = {"Content-Type": "application/json"}
        self.content_result: List[Dict[str, Any]] = []
        self.account_result: Dict[str, Any] = {}

    def get_articles_list(self) -> None:
        """
        获取文章数据
        """
        json_data = {}
        url = "https://api.juejin.cn/content_api/v1/article/query_list"
        payload = {"user_id": self.user_id, "sort_type": 2}
        rs = self.request_data(
            "POST", url=url, data=json.dumps(payload), headers=self.headers
        )
        if rs:
            json_data = rs.json()
            if not json_data.get("data") or json_data["err_msg"] != "success":
                return
        data = json_data["data"]
        for article in data:
            source_id = article["article_id"]
            self.content_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": article["article_id"],
                    "clicks_count": article["article_info"]["view_count"],
                    "like_count": article["article_info"]["digg_count"],
                    "comment_count": article["article_info"]["comment_count"],
                    "summary": article["article_info"]["title"],
                    "url": f"https://juejin.cn/post/{source_id}",
                    "publish_time": datetime.fromtimestamp(
                        int(article["article_info"]["ctime"])
                    ),
                    "publish_date": datetime.fromtimestamp(
                        int(article["article_info"]["ctime"])
                    ).date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(data)} article data finish.")

    def get_account_info(self) -> None:
        json_data = {}
        self.account_result = {
            "platform": self.platform,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        params = {"aid": 2608, "user_id": self.user_id, "not_self": 1}
        url = "https://api.juejin.cn/user_api/v1/user/get"
        rs = self.request_data(url=url, params=params)
        if rs:
            json_data = rs.json()
            if json_data.get("err_msg") != "success":
                return
        fans = str(json_data.get("data", {}).get("follower_count", "-1"))
        self.account_result["fans"] = fans
        self.account_result["value"] = json_data.get("data", {}).get("power", "-1")
        self.log.info(f"Download {self.platform} account data finish.")

    def get_hotspot_list(self) -> None:
        """
        获取沸点数据
        """
        json_data = {}
        url = "https://api.juejin.cn/content_api/v1/short_msg/query_list"
        payload = {"sort_type": 4, "user_id": self.user_id}
        rs = self.request_data(
            "POST", url=url, data=json.dumps(payload), headers=self.headers
        )
        if rs:
            json_data = rs.json()
            if not json_data.get("data") or json_data["err_msg"] != "success":
                return
        data = json_data["data"]
        for essay in data:
            self.content_result.append(
                {
                    "content_type": "pin",
                    "platform": self.platform,
                    "source_id": essay["msg_id"],
                    "like_count": essay["msg_Info"]["digg_count"],
                    "comment_count": essay["msg_Info"]["comment_count"],
                    "summary": essay["msg_Info"]["content"][:50].strip(),
                    "publish_time": datetime.fromtimestamp(
                        int(essay["msg_Info"]["ctime"])
                    ),
                    "publish_date": datetime.fromtimestamp(
                        int(essay["msg_Info"]["ctime"])
                    ).date(),
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(data)} pin data finish.")

    def _start(self) -> None:
        self.get_articles_list()
        self.get_hotspot_list()
        self.get_account_info()
        if not self.account_result or not self.content_result:
            raise Exception(
                f"Empty account: {self.account_result},"
                f" content: {self.content_result[:3]}"
            )
        with get_db() as db:
            insert_account(db, self.account_result)
            for item in self.content_result:
                upinsert_content(db, item)
        self.log.info(
            f"Save {len(self.content_result)} content "
            f"| account: {self.account_result} data."
        )
