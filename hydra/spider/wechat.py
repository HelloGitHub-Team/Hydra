#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-05 21:47
#   Desc    :   公众号平台
import datetime
import hashlib
from operator import itemgetter
from random import Random
from typing import Any, Dict, List

from hydra.config import Config
from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


class WeChat(BaseSpider):
    def __init__(self) -> None:
        super(WeChat, self).__init__()
        self.platform, self.account, self.token = Config.wechat()

    @staticmethod
    def random_str(random_len: int = 9) -> str:
        """
        生成随机数
        :param random_len: 长度
        """
        result = ""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        length = len(chars) - 1
        random = Random()
        for i in range(random_len):
            result += chars[random.randint(0, length)]
        return result

    @staticmethod
    def md5(input_str: str) -> str:
        """
        MD5 加密方法
        """
        m = hashlib.md5()
        m.update(input_str.encode("utf-8"))
        return m.hexdigest()

    def generate_params(self, url_path: str, params: dict) -> dict:
        """
        生成加密参数
        """
        sign_str = url_path + "?AppKey=joker&"
        items = sorted(params.items(), key=itemgetter(0))
        for key, value in items:
            param = key + "=" + value + "&"
            if key != "nonce" and key != "xyz":
                sign_str += param
        params["nonce"] = self.random_str()
        sign_str += "nonce=" + params["nonce"]
        xyz = self.md5(sign_str)
        params["xyz"] = xyz
        return params

    def request_newrank(
        self, url_path: str, method: str = "POST", **kwargs: Any
    ) -> dict:
        """
        请求 newrank
        :param url_path: PATH
        :param method: HTTP method
        """
        url = "https://www.newrank.cn" + url_path
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1)"
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.88 Safari/537.36",
            "authority": "www.newrank.cn",
        }
        cookies = {"token": self.token}
        kwargs.update({"account": self.account})
        params = self.generate_params(url_path, kwargs)
        response = self.request_data(
            url=url, method=method, params=params, headers=headers, cookies=cookies
        )
        if response:
            return response.json()
        else:
            return dict()

    def get_account_info(self) -> list:
        rank_path = "/xdnphb/detail/v1/rank/data/rankings"
        fans_path = "/xdnphb/detail/v1/rank/head/getEstimateFansNum"

        rank_data = self.request_newrank(rank_path, type="day")
        fans_data = self.request_newrank(fans_path)
        get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rank_result: List[Dict[str, Any]] = []

        if not rank_data["success"] or not fans_data["success"]:
            self.log.error(f"POST {rank_path} or {fans_path}: No Data.")
            return rank_result
        fans = int(fans_data["value"]["fullAvg_read"].replace(",", ""))
        rank_list = rank_data["value"]
        for rank_item in rank_list:
            rank_result.append(
                {
                    "platform": self.platform,
                    "fans": fans,
                    "value": rank_item.get("log1p_mark", -1),
                    "rank": rank_item.get("rank_position", -1),
                    "update_date": rank_item.get("rank_date", None),
                    "get_time": get_time,
                }
            )
        self.log.info(f"Download {len(rank_result)} info data finish.")
        return rank_result

    def get_articles_list(self) -> list:
        """
        获取公众号文章的数据
        :return:
        [{'clicks_count': 6558,
         'is_original': 1,
         'is_head': 1,
         'share_count': 28,
         'like_count': 0,
         'comment_count': 0,
         'public_time': '2021-01-04 08:15:00',
         'title': '我们月刊最受欢迎的开源项目 Top10（2020 年）',
         'update_time': '2021-01-07 13:32:15',
         'url': 'https://mp.weixin.qq.com/xxx'}..]
        """
        url_path = "/xdnphb/detail/v1/rank/article/lists"
        articles_data = self.request_newrank(url_path)
        articles_result: List[Dict[str, Any]] = []
        if not articles_data["success"]:
            self.log.error(f"POST {url_path}: No Data.")
            return articles_result
        get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        articles_list = articles_data["value"]["articles"]
        for day_articles in articles_list:
            for article in day_articles:
                public_date = article.get("publicTime").split(" ")[0]
                articles_result.append(
                    {
                        "content_type": "article",
                        "platform": self.platform,
                        "source_id": article.get("uuid"),
                        "clicks_count": article.get("clicksCount", -1),
                        "share_count": article.get("likeCount", -1),
                        # 在看相当于分享
                        "is_original": article.get("originalFlag", 0),
                        "is_head": int(article.get("orderNum") == 0),
                        "summary": article.get("title"),
                        "url": article.get("url"),
                        "public_time": article.get("publicTime"),
                        "public_date": public_date,
                        "update_time": article.get("updateTime"),
                        "get_time": get_time,
                    }
                )
        self.log.info(f"Download {len(articles_result)} article data finish.")
        return articles_result

    def _start(self) -> None:
        articles_list = self.get_articles_list()
        account_info_list = self.get_account_info()
        with get_db() as db:
            for account_info in account_info_list:
                insert_account(db, account_info)
            for article in articles_list:
                upinsert_content(db, article)
        if not articles_list or not account_info_list:
            raise Exception
