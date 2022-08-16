# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: throttle.py
@Time: 2022/7/1823:26
@Software: PyCharm
"""

from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    """ Visit throttle"""
    scope = "visit"

    def get_cache_key(self, request, view):
        key = request.META.get("REMOTE_ADDR")
        return key
