# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: plugins.py
@Time: 2022/7/230:31
@Software: PyCharm
"""

import hashlib
import time

from django.conf import settings


def get_token(user: str) -> str:
    """ sha256 for token """
    ctime = str(time.time())
    obj = hashlib.sha256(bytes(user, encoding="utf-8"))
    obj.update(bytes(ctime, encoding="utf-8"))
    return "Token " + obj.hexdigest()


def myhash(pwd) -> str:
    """ sha256 for password"""
    obj = hashlib.sha256(bytes(settings.SECRET_KEY, encoding="utf-8"))
    obj.update(bytes(pwd, encoding="utf-8"))
    return obj.hexdigest()
