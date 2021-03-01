#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-23 22:04
#   Desc    :   今日头条
import datetime
import json
import os
from typing import Any, Dict, List

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
        self.user_token = Config.toutiao()

    def get_articles_list(self) -> list:
        """
        获取文章数据
        """
        url = "https://www.toutiao.com/api/pc/feed/"
        json_data = dict()
        articles_result: List[Dict[str, Any]] = []
        rs = self.request_data(
            url=url,
            params={
                "category": "pc_profile_article",
                "utm_source": "toutiao",
                "visit_user_token": self.user_token,
                "max_behot_time": 0,
                "_signature": self.signature(url),
            },
        )
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return articles_result
        for item in json_data.get("data", []):
            clicks_count = item["go_detail_count"]
            if clicks_count.count("万") > 0:
                clicks_count = int(float(clicks_count.replace("万", "")) * 10000)
            source_id = item["group_id"]
            article = {
                "content_type": "article",
                "platform": self.platform,
                "source_id": source_id,
                "clicks_count": clicks_count,
                "comment_count": item["comments_count"],
                "summary": item["title"],
                "url": f"https://www.toutiao.com/a{source_id}/",
                "get_time": self.get_time,
                "update_time": self.get_time,
            }
            # 未获取到详细的发布时间，所以只能判断一天内的发布时间
            # 超过一天的只更新不插入
            if item["behot_time"] == "1天内":
                article["publish_time"] = self.get_date + " 08:50:00"
                article["publish_date"] = self.get_date
            articles_result.append(article)
        self.log.info(f"Download {len(articles_result)} article data finish.")
        return articles_result

    def get_pin_list(self) -> list:
        """
        获取微头条数据
        """
        url = "https://www.toutiao.com/api/pc/feed/"
        json_data = {}
        micros_result: List[Dict[str, Any]] = []
        rs = self.request_data(
            url=url,
            params={
                "category": "pc_profile_ugc",
                "utm_source": "toutiao",
                "visit_user_token": self.user_token,
                "max_behot_time": 0,
                "_signature": self.signature(url),
            },
        )
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return micros_result
        for item in json_data.get("data", []):
            publish_datetime = datetime.datetime.fromtimestamp(
                int(item["base_cell"]["log_pb"]["create_time"])
            )
            source_id = item["concern_talk_cell"]["id"]
            item_detail = json.loads(item["concern_talk_cell"]["packed_json_str"])
            summary = item_detail["content"][:50].strip()
            clicks_count = item_detail["read_count"]
            if clicks_count.count("万") > 0:
                clicks_count = int(float(clicks_count.replace("万", "")) * 10000)
            micro = {
                "content_type": "pin",
                "platform": self.platform,
                "source_id": source_id,
                "clicks_count": clicks_count,
                "like_count": item_detail["digg_count"],
                "comment_count": item_detail["comment_count"],
                "summary": summary,
                "url": f"https://www.toutiao.com/w/a{source_id}/",
                "publish_time": publish_datetime,
                "publish_date": publish_datetime.date(),
                "get_time": self.get_time,
                "update_time": self.get_time,
            }
            micros_result.append(micro)
        self.log.info(f"Download {len(micros_result)} pin data finish.")
        return micros_result

    def get_account_info(self) -> dict:
        url = "https://www.toutiao.com/api/pc/user/fans_stat"
        json_data = {}
        account_result: Dict[str, Any] = {
            "platform": self.platform,
            "fans": -1,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        rs = self.request_data(
            url=url,
            method="POST",
            params={"_signature": self.signature(url)},
            data={"token": self.user_token},
        )
        if rs:
            json_data = rs.json()
            if json_data["message"] != "success":
                return account_result
        fans = json_data.get("data", {}).get("fans", "-1")
        if fans.count("万") > 0:
            fans = int(float(fans.replace("万", "")) * 10000)
        account_result["fans"] = fans
        self.log.info(f"Download {self.platform} account data finish.")
        return account_result

    @staticmethod
    def signature(url: str) -> str:
        js_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "js/tt_signature.js"
        )
        result = os.popen(f"node {js_file_path} {url}").read()
        return result

    def _start(self) -> None:
        articles_list = self.get_articles_list()
        micros_list = self.get_pin_list()
        account_info = self.get_account_info()
        if not articles_list or not account_info or not micros_list:
            raise Exception
        with get_db() as db:
            insert_account(db, account_info)
            for article in articles_list:
                upinsert_content(db, article)
            for micro in micros_list:
                upinsert_content(db, micro)
