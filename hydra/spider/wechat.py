#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-05 21:47
#   Desc    :   公众号平台
import datetime
import hashlib
from random import Random
from typing import Any, Dict, List

from hydra.config import Config
from hydra.db.base import get_db
from hydra.db.curd import upinsert_article
from hydra.spider.base import BaseSpider


class WeChat(BaseSpider):
    def __init__(self) -> None:
        super(WeChat, self).__init__()
        self.platform = 1
        self.account, self.token = Config.wechat()

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
        items = params.items()
        for key, value in items:
            param = key + "=" + value + "&"
            if key != "nonce" and key != "xyz":
                sign_str += param
        params["nonce"] = self.random_str()
        sign_str += "nonce=" + params["nonce"]
        xyz = self.md5(sign_str)
        params["xyz"] = xyz
        return params

    def get_account_info(self) -> dict:
        pass

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
         'url': 'https://mp.weixin.qq.com/xxx'},..]
        """
        requests_path = "/xdnphb/detail/v1/rank/article/lists"

        url = "https://www.newrank.cn" + requests_path
        method = "POST"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1)"
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.88 Safari/537.36",
            "authority": "www.newrank.cn",
        }
        cookies = {"token": self.token}
        params = self.generate_params(requests_path, {"account": self.account})
        response = self.request_data(
            url=url, method=method, params=params, headers=headers, cookies=cookies
        )
        articles_result: List[Dict[Any, Any]] = []
        if response is None:
            return articles_result
        resp_dict = response.json()
        if not resp_dict["success"]:
            self.log.error(f"{method} {url} :No Data.")
            raise Exception
        get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        articles_list = resp_dict["value"]["articles"]
        for day_articles in articles_list:
            for article in day_articles:
                articles_result.append(
                    {
                        "content_type": 1,
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
                        "update_time": article.get("updateTime"),
                        "get_time": get_time,
                    }
                )
        self.log.info(f"Download {len(articles_result)} article data.")
        return articles_result

    def _start(self) -> None:
        articles_list = self.get_articles_list()
        with get_db() as db:
            for article in articles_list:
                upinsert_article(db, article)
