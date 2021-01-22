#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-18 23:30
#   Desc    :   工具类方法
import datetime
import random
import string

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def random_lower_string(k: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_int(k: int = 1) -> int:
    return random.randrange(k)


def random_bigint(k: int = 1) -> int:
    return random.randrange(10 ** k)


def random_float(k: int = 1) -> float:
    return random.random() * (10 ** k)


def random_url() -> str:
    return (
        f"https://{random_lower_string()}.com/"
        f"{random_lower_string(3)}?{random_lower_string(50)}"
    )


def random_datetime_str() -> str:
    return datetime.datetime.now().strftime(TIME_FORMAT)


def random_date_str() -> str:
    return datetime.datetime.now().strftime(DATE_FORMAT)


def random_gbk2312(k: int = 4) -> str:
    result = ""
    for i in range(k):
        result += chr(random.randint(0x4E00, 0x9FBF))
    return result
