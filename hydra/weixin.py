#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-05 21:47
#   Desc    :
import requests


def get_article_list(account, token):
    url = "https://www.newrank.cn/xdnphb/detail/v1/rank/article/lists"
    params = {""}
    response = requests.post(url, params=params)
    resp_dict = response.json()
    return resp_dict


if __name__ == "__main__":
    account = "1"
    token = "2"
    print(get_article_list(account, token))
