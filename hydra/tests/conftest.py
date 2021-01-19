#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2021-01-19 00:09
#   Desc    :   测试通用的部分
import time
from typing import Generator

import pytest

from hydra.db.base import get_db
from hydra.tests.utils.utils import DATE_FORMAT


@pytest.fixture(scope="session", autouse=True)
def timer_session_scope():
    start = time.time()
    print("\nstart: {}".format(time.strftime(DATE_FORMAT, time.localtime(start))))
    yield

    finished = time.time()
    print("finished: {}".format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print("Total time cost: {:.3f}s".format(finished - start))


@pytest.fixture(autouse=True)
def timer_function_scope(request):
    start = time.time()
    yield
    print("{} Time cost: {:.3f}s".format(request.node.name, time.time() - start))


@pytest.fixture(scope="session")
def db() -> Generator:
    with get_db() as db:
        yield db
