#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-21 15:57
#   Desc    :
import datetime
import random
import time
from typing import Any, Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter

from hydra.utils import logger

# requests.packages.urllib3.disable_warnings()


class BaseSpider(object):
    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.log = logger
        self.token_header: Dict[str, str] = dict()
        self.get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.get_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=3))

    @property
    def today(self) -> datetime.date:
        return datetime.date.today()

    @staticmethod
    def random_agent() -> str:
        user_agent = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        ]
        return random.choice(user_agent)

    def request_data(
        self, method: Union[str, bytes] = "GET", **kwargs: Any
    ) -> Optional[requests.Response]:
        method = str(method)
        url = kwargs.pop("url")
        if not kwargs.get("timeout"):
            kwargs["timeout"] = (5, 5)
        if not kwargs.get("headers"):
            kwargs["headers"] = {"user-agent": self.random_agent()}
        # 过滤敏感信息，防止打到日志中
        args_list = []
        for k, v in kwargs.items():
            if k == "data" or k == "cookies" or k == "headers":
                continue
            # if isinstance(v, dict) and (("Authorization" in v) or ("token" in v)):
            #     continue
            args_list.append("{}: {}".format(k, v))
        args_str = "{" + ",".join(args_list) + "}"
        try:
            s_time = time.time()
            if method.upper() == "GET":
                response = self.session.get(url, **kwargs)
            else:
                response = self.session.post(url, **kwargs)
            speed_time = round(time.time() - s_time, 2)
            if response.status_code == 200:
                self.log.info(
                    f"{self.name} {method.upper()} {url} "
                    f"{speed_time}s {args_str} {response.status_code}"
                )
                return response
            else:
                self.log.info(
                    f"{self.name} {method.upper()} {url} {args_str}"
                    f" {response.status_code} {speed_time}s "
                    f"ERROR: {str(response.content)}."
                )
                return None
        except Exception as e:
            self.log.exception(e)
            self.log.error(f"{method.upper()} {url} {args_str} FAIL. {e}")
            return None

    def _start(self) -> None:
        pass

    def start(self) -> None:
        try:
            s_time = time.time()
            self._start()
            e_time = time.time()
            self.log.info(
                "{} spider success speed {}s.".format(
                    self.name, round((e_time - s_time), 2)
                )
            )
        except Exception as e:
            self.log.exception(e)
            self.log.error("{} spider error. {}".format(self.name, e))
