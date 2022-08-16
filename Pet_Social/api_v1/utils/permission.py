# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: permission.py
@Time: 2022/7/1823:18
@Software: PyCharm
"""

from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    """ owner permission """
    message = "No Permission"

    def has_permission(self, request, view):
        """ view is owner filtered through url params """
        if request.user != str(view.kwargs["pk"]):
            return False
        return True
