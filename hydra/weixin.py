#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-05 21:47
#   Desc    :   基于新榜的公众号文章阅读数监控
import hashlib
from random import Random

import requests


# 生成随机数
def random_str(randomlength=9):
    result = ""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        result += chars[random.randint(0, length)]
    return result


# md5加密方法
def md5(input_str):
    m = hashlib.md5()
    m.update(input_str.encode("utf-8"))
    return m.hexdigest()


# 获取加密参数
def get_params(url, params):
    sign_str = url + "?AppKey=joker&"
    items = params.items()
    for key, value in items:
        param = key + "=" + value + "&"
        if key != "nonce" and key != "xyz":
            sign_str += param
    params["nonce"] = random_str()
    sign_str += "nonce=" + params["nonce"]
    xyz = md5(sign_str)
    params["xyz"] = xyz
    return params


def get_article_list(account:str, token:str):
    """
    :return:
    [{'clicks_count': 6558,
     'is_original': 1,
     'like_count': 28,
     'public_time': '2021-01-04 08:15:00',
     'title': '我们月刊最受欢迎的开源项目 Top10（2020 年）',
     'update_time': '2021-01-07 13:32:15',
     'url': 'https://mp.weixin.qq.com/xxx'},..]
    """
    requests_path = "/xdnphb/detail/v1/rank/article/lists"

    url = "https://www.newrank.cn" + requests_path

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1)"
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36",
        "authority": "www.newrank.cn",
    }
    cookies = {"token": token}
    params = get_params(requests_path, {"account": account})
    response = requests.post(url, params=params, headers=headers,
                             cookies=cookies)
    articles_result = []
    try:
        resp_dict = response.json()
        if not resp_dict["success"]:
            raise Exception

        articles_list = resp_dict["value"]["articles"]
        for day_articles in articles_list:
            for article in day_articles:
                articles_result.append(
                    {
                        "clicks_count": article.get("clicksCount", -1),
                        "like_count": article.get("likeCount", -1),
                        "is_original": article.get("originalFlag", 0),
                        "public_time": article.get("publicTime"),
                        "title": article.get("title"),
                        "url": article.get("url"),
                        "update_time": article.get("updateTime"),
                    }
                )
        print("Get {} article data.".format(len(articles_result)))
        return articles_result
    except Exception as e:
        print("Reqeust {} error: {}".format(url, e))


if __name__ == "__main__":
    account = "GitHub520"
    token = ""
    get_article_list(account, token)
