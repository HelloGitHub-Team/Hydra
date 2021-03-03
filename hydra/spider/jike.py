#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-02-28 23:33
#   Desc    :   即刻
import datetime
from typing import Tuple

from requests_html import HTML, HtmlElement

from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


class Jike(BaseSpider):
    def __init__(self) -> None:
        super(Jike, self).__init__()
        self.platform = "jike"
        self.host = "https://web.okjike.com"
        self.user_id = "ff31a838-6eb9-440d-9970-dabc5b2c0309"

    @staticmethod
    def _parse(item: HtmlElement) -> Tuple[int, int, int]:
        like_count = 0
        comment_count = 0
        share_count = 0
        like_el = item.xpath(
            '//div[@class="sc-bdfBwQ sc-gsTCUz hkfshi bhdLno"]/div/'
            'span[@class="Like___StyledSpan-sc-8xi69i-1 flDnWd"]'
        )
        if like_el:
            like_count = int(like_el[0].text.strip())
        comment_el = item.xpath(
            '//div[@class="sc-bdfBwQ sc-gsTCUz hkfshi bhdLno"]/div/'
            'span[@class="Comment___StyledSpan-sc-4djxqy-1 eowffA"]'
        )
        if comment_el:
            comment_count = int(comment_el[0].text.strip())
        share_el = item.xpath(
            '//div[@class="sc-bdfBwQ sc-gsTCUz hkfshi bhdLno"]/div/'
            'span[@class="Share___StyledSpan-qfhiuf-1 eSDvno"]'
        )
        if share_el:
            share_count = int(share_el[0].text.strip())
        return like_count, comment_count, share_count

    def get_all_info(self) -> None:
        url = f"{self.host}/u/{self.user_id}"
        rs = self.request_data(url=url)
        if rs is None:
            return
        html = HTML(html=rs.text)
        fans = int(
            html.xpath(
                '//div[@class="sc-bdfBwQ sc-gsTCUz ' 'bedXUN bhdLno"]/a[2]/span'
            )[0].text.strip()
        )
        self.account_result = {
            "platform": self.platform,
            "fans": fans,
            "get_time": self.get_time,
            "update_date": self.get_date,
        }
        self.log.info(f"Download {self.platform} account data finish.")
        pin_result = html.xpath(
            '//div[@class="sc-bdfBwQ sc-gsTCUz '
            'Main-sc-5q3zjg-0 jzXtZT bhdLno JLHxz"]/div/div/div'
        )
        for item in pin_result:
            path_str = (
                item.xpath(
                    '//div[@class="sc-bdfBwQ hMCytU MessageHeader'
                    '___StyledText-sc-7fr80f-4 ixrlxw"]/a'
                )[0]
                .attrs["href"]
                .strip()
            )
            url = f"{self.host}{path_str}"
            source_id = path_str.split("/")[-1]
            datetime_str = item.xpath(
                '//div[@class="sc-bdfBwQ hMCytU MessageHeader'
                '___StyledText-sc-7fr80f-4 ixrlxw"]/a/time'
            )[0].attrs["datetime"]
            publish_time = datetime.datetime.strptime(
                datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ"
            ) + datetime.timedelta(hours=8)
            publish_date = publish_time.date()
            content = (
                item.xpath('//div[@class="sc-bdfBwQ jzXtZT"]/div')[0].text[:50].strip()
            )
            like_count, comment_count, share_count = self._parse(item)
            self.content_result.append(
                {
                    "content_type": "pin",
                    "platform": self.platform,
                    "source_id": source_id,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "share_count": share_count,
                    "summary": content,
                    "url": url,
                    "publish_time": publish_time,
                    "publish_date": publish_date,
                    "get_time": self.get_time,
                    "update_time": self.get_time,
                }
            )
        self.log.info(f"Download {len(self.content_result)} pin data finish.")

    def _start(self) -> None:
        self.get_all_info()
        if not self.result_is_empty():
            with get_db() as db:
                insert_account(db, self.account_result)
                for pin in self.content_result:
                    upinsert_content(db, pin)
        self.log.info(
            f"Save {self.name} content: {len(self.content_result)} "
            f"| account: {self.account_result} data finish."
        )
