# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: auth.py
@Time: 2022/7/1823:08
@Software: PyCharm
"""

from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication, exceptions


class LoginAuthentication(BaseAuthentication):
    """ login authenticate, base token """

    def authenticate(self, request):
        # get token, from HTTP header
        token = request.META.get("HTTP_AUTHORIZATION")
        uid = request.META.get("HTTP_UID")
        # validate token by cache
        token_obj = cache.get(uid)
        if not token_obj or token_obj != token:
            raise exceptions.AuthenticationFailed("Please login!")

        return uid, token_obj
