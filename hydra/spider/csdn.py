#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-22 15:36
#   Desc    :   CSDN
from typing import Any, Dict, List, Tuple

from requests_html import HTML

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


"""
https://hellogithub.blog.csdn.net/
"""


class Csdn(BaseSpider):
    def __init__(self) -> None:
        super(Csdn, self).__init__()
        self.platform = "csdn"
        self.blog_url = "https://blog.csdn.net/a419240016"

    def get_articles_list(self) -> Tuple[list, dict]:
        """
        获取文章数据
        """
        articles_result: List[Dict[str, Any]] = []
        rs = self.request_data(url=self.blog_url)
        if rs is None:
            return [], {}
        html = HTML(html=rs.text)
        div_list = html.xpath(
            '//*[@id="articleMeList-blog"]/div[@class="article-list"]/div'
        )
        for div_item in div_list:
            is_original = bool(div_item.xpath("//h4/a/span")[0].text == "原创")
            url = div_item.xpath("//h4/a")[0].attrs["href"]
            title = "".join(div_item.xpath("//h4/a/text()")).strip()
            div_item.xpath('//div[@class="info-box d-flex align-content-center"]')
            publish_time = div_item.xpath('//span[@class="date"]')[0].text
            publish_date = publish_time.split(" ")[0]
            clicks_count = div_item.xpath('//span[@class="read-num"]')[0].text
            try:
                comment_count = div_item.xpath('//span[@class="read-num"]')[1].text
            except Exception:
                comment_count = 0
            source_id = div_item.attrs["data-articleid"]
            articles_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": source_id,
                    "clicks_count": clicks_count,
                    "comment_count": comment_count,
                    "is_original": is_original,
                    "summary": title,
                    "url": url,
                    "publish_time": publish_time,
                    "publish_date": publish_date,
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(articles_result)} article data finish.")
        profile_div = html.xpath(
            '//*[@id="asideProfile"]/div[@class="data-info d-flex item-tiling"]/dl'
        )
        account_result: Dict[str, Any] = {
            "platform": self.platform,
            "fans": int(profile_div[6].attrs["title"]),
            "value": int(profile_div[5].attrs["title"]),
            "rank": int(profile_div[2].attrs["title"]),
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        return articles_result, account_result

    def _start(self) -> None:
        articles_list, account_info = self.get_articles_list()
        if not articles_list or not account_info:
            raise Exception
        with get_db() as db:
            insert_account(db, account_info)
            for article in articles_list:
                upinsert_content(db, article)
