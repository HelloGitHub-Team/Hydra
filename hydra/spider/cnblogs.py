#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-22 15:36
#   Desc    :
from typing import Any, Dict, List

from requests_html import HTML

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


"""
https://www.cnblogs.com/xueweihan/
"""


class Cnblogs(BaseSpider):
    def __init__(self) -> None:
        super(Cnblogs, self).__init__()
        self.platform = "cnblogs"
        self.blog_url = "https://www.cnblogs.com/xueweihan/"

    def get_articles_list(self) -> list:
        """
        获取文章数据
        """
        articles_result: List[Dict[str, Any]] = []
        rs = self.request_data(url=self.blog_url)
        if rs is None:
            return articles_result
        html = HTML(html=rs.text)
        div_list = html.xpath('//*[@id="mainContent"]/div/div[@class="day"]')
        for div_item in div_list:
            title_div = div_item.xpath('//div[@class="postTitle"]/a')[0]
            url = title_div.attrs["href"]
            title = title_div.xpath("//span/text()")[-1].strip()
            publish_time = (
                div_item.xpath('//div[@class="postDesc"]/text()')[0]
                .replace("posted @ ", "")
                .replace("削微寒", "")
                .strip()
            )
            publish_date = publish_time.split(" ")[0]
            source_id = div_item.xpath('//div[@class="postDesc"]/span')[0].attrs[
                "data-post-id"
            ]
            clicks_count = int(
                div_item.xpath(
                    '//div[@class="postDesc"]/span[@class="post-view-count"]'
                )[0].search("阅读({})")[0]
            )
            like_count = int(
                div_item.xpath(
                    '//div[@class="postDesc"]/span[@class="post-digg-count"]'
                )[0].search("推荐({})")[0]
            )
            comment_count = int(
                div_item.xpath(
                    '//div[@class="postDesc"]/span[@class="post-comment-count"]'
                )[0].search("评论({})")[0]
            )
            articles_result.append(
                {
                    "content_type": "article",
                    "platform": self.platform,
                    "source_id": source_id,
                    "clicks_count": clicks_count,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "summary": title,
                    "url": url,
                    "publish_time": publish_time,
                    "publish_date": publish_date,
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(articles_result)} article data finish.")
        return articles_result

    def get_account_info(self) -> dict:
        account_result: Dict[str, Any] = {
            "platform": self.platform,
            "fans": -1,
            "value": -1,
            "rank": -1,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }

        rs = self.request_data(url="https://www.cnblogs.com/xueweihan/ajax/news.aspx")
        if rs is None:
            return {}
        html = HTML(html=rs.text)
        account_result["fans"] = int(
            html.xpath(
                '//*[@id="profile_block"]/a[@href="'
                'https://home.cnblogs.com/u/xueweihan/followers/"]'
            )[0].text
        )
        rs = self.request_data(
            url="https://www.cnblogs.com/xueweihan/ajax/sidecolumn.aspx"
        )
        html = HTML(html=rs.text)
        account_result["value"] = int(
            html.xpath('//*[@id="sidebar_scorerank"]/div/ul/li' '[@class="liScore"]')[
                0
            ].text.replace("积分 - ", "")
        )
        account_result["rank"] = int(
            html.xpath('//*[@id="sidebar_scorerank"]/div/ul/li' '[@class="liRank"]')[
                0
            ].text.replace("排名 - ", "")
        )
        return account_result

    def _start(self) -> None:
        articles_list = self.get_articles_list()
        account_info = self.get_account_info()
        if not articles_list or not account_info:
            raise Exception
        with get_db() as db:
            insert_account(db, account_info)
            for article in articles_list:
                upinsert_content(db, article)
