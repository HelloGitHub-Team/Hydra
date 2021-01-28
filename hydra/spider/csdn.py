#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   notfresh
#   E-mail  :   1195056983@qq.com
#   Date    :   2021-01-28 19:18:16
#   Desc    :   CSDN
import datetime
import hashlib
from operator import itemgetter
from random import Random
from typing import Any, Dict, List, Tuple

import time

import requests
from scrapy.selector import Selector # 用于以低成本的方式转移scrapy框架解析html

from hydra.config import Config
from hydra.db.base import get_db
from hydra.db.curd import insert_account, upinsert_content
from hydra.spider.base import BaseSpider


class CSDN(): # BaseSpider
    def __init__(self) -> None:
        super(CSDN, self).__init__()
        self.num_in_page = 40
        self.first_page = True
        self.articles_list = []
        self.account_info_list = []

    @staticmethod
    def md5(input_str: str) -> str:
        """
        MD5 加密方法
        """
        m = hashlib.md5()
        m.update(input_str.encode("utf-8"))
        return m.hexdigest()

    def get_articles_list(self) -> Tuple[list, list]:
        """
        获取公众号文章的数据以及作者本人的数据,比如阅读量,粉丝数量等等
        
        demo:
        :return:
        
        [
            {'clicks_count': 6558,
         'is_original': 1,
         'is_head': 1,
         'share_count': 28,
         'like_count': 0,
         'comment_count': 0,
         'public_time': '2021-01-04 08:15:00',
         'title': '我们月刊最受欢迎的开源项目 Top10（2020 年）',
         'update_time': '2021-01-07 13:32:15',
         'url': 'https://mp.weixin.qq.com/xxx'}..
         ]

        [{'original_count': '226', 
        'rank_weekly': '573', 
        'rank_totally': '10379', 
        'click_count': '322403', 
        'level': '6级', 
        'membership_point': '5276', 
        'fans_count':'1718', 
        'thumbup_count': '1179', 
        'comment_count': '331', 
        'collect_count': '5082'}]

        """
        url = "https://hellogithub.blog.csdn.net/article/list/{}"
        page_num = 1
        self.parse(url, page_num)
        return self.articles_list, self.account_info_list


    def _start(self) -> None:        
        articles_list = self.get_articles_list()
        account_info_list = self.get_account_info()
        with get_db() as db:
            for article in articles_list:
                upinsert_content(db, article)
            for account_info in account_info_list:
                insert_account(db, account_info)
        if not articles_list or not account_info_list:
            raise Exception


    def parse(self, list_url: str, page_num: int) -> None:
        """
        这个方法用来获取文章列表, 根据列表初步获得一些文章的信息
        它会根据有多少页, 从而直接访问指定页码的列表

        list_url: 列表页url模板
        page_num: 页码号

        """
        list_url2 = list_url.format(page_num)
        res = requests.get(list_url2)
        r = Selector(text=res.text)
        author = r.xpath('//div[@class="profile-intro-name-boxTop"]/a[1]/@title').extract_first()

        # 以下这一段是为了获取在CSDN上的用户统计信息
        account_info = {}
        original_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][1]/dl[@class="text-center"][1]/@title').extract_first()
        rank_weekly = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][1]/dl[@class="text-center"][2]/@title').extract_first()
        rank_totally = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][1]/dl[@class="text-center"][3]/@title').extract_first()
        click_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][1]/dl[@class="text-center"][4]/@title').extract_first()
        level = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][1]/dl[@class="text-center"][5]/@title').extract_first()[:2]

        membership_point = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][2]/dl[@class="text-center"][1]/@title').extract_first()
        fans_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][2]/dl[@class="text-center"][2]/@title').extract_first()
        thumbup_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][2]/dl[@class="text-center"][3]/@title').extract_first()
        comment_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][2]/dl[@class="text-center"][4]/@title').extract_first()
        collect_count = r.xpath('//div[@id="asideProfile"]//div[contains(@class,"data-info")][2]/dl[@class="text-center"][5]/@title').extract_first()

        account_info['platform'] = 'csdn'
        account_info['original_count'] = original_count
        account_info['rank'] = rank_weekly
        account_info['rank_weekly'] = rank_weekly
        account_info['rank_totally'] = rank_totally
        account_info['click_count'] = click_count
        account_info['level'] = level
        account_info['value'] = membership_point
        account_info['fans'] = fans_count
        account_info['thumbup_count'] = thumbup_count
        account_info['comment_count'] = comment_count
        account_info['collect_count'] = collect_count
        self.account_info_list.append(account_info) # 虽然只有一个元素,但是为了适配那个方法,就写成这样了
        print('*' * 100)
        print(account_info)
        print('*' * 100)

        posts = r.xpath('//div[@class="article-list"]/div')
        for post in posts:
            url = post.xpath('./h4/a/@href').extract_first()
            type = post.xpath('./h4/a/span[contains(@class, "article-type")]/text()').extract_first()
            try:
                title = post.xpath('./h4/a/text()').re('^\s*(.+)\s*$')[1]
            except:
                title = '标题解析失败'
            date_ = post.xpath('.//span[@class="date"]/text()').extract_first()
            read_num = post.xpath('.//span[@class="read-num"][1]/text()').extract_first()
            comment_num = post.xpath('.//span[@class="read-num"][2]/text()').extract_first() or 0
            item = {
                'url': url,
                'is_original': 1 if type=='原创' else 0,
                'summary': title,
                'public_time': date_,
                'clicks_count': read_num,
                'comment_count': comment_num,
                'author': author,
                'platform': 'csdn',
                'content_type': '文章',
                'source_id': self.md5(url)
            }
            self.parse_detail(url=url, data=item)

        # 多页爬取
        cnt = r.xpath('//ul[@class="container-header-ul"]/li[1]/span/text()').re_first('\d+')
        cnt = int(cnt)
        page = cnt // self.num_in_page + 1
        if self.first_page:
            self.first_page = False
            for i in range(2, page+1):
                time.sleep(1)
                self.parse(list_url, i)


    def parse_detail(self, url: str, data: dict)->None:
        """
        这个方法的作用是进入每篇文章获得更详细的数据

        url: 每篇文章的url
        data: 已经获得的局部数据

        """
        res = requests.get(url)
        r = Selector(text=res.text)
        item = data
        toolbox =  r.xpath('//ul[@class="toolbox-list"]')
        try:
            like_num = toolbox.xpath('./li[contains(@class, "is-like")]//span[@class="count"]/text()').re_first('(\d+)') or 0
        except:
            like_num = 0
        try:
            favorite_num = toolbox.xpath(toolbox.xpath('.//*[@id="get-collection"]/text()').re_first('(\d+)')).re_first('(\d+)') or 0
        except:
            favorite_num = 0
        item['like_count'] = like_num
        item['collect_count'] = favorite_num
        print(item)
        self.articles_list.append(item)


if __name__ == '__main__':
    csdn = CSDN()
    csdn._start()