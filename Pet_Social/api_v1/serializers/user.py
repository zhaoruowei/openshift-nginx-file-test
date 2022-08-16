# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: user.py
@Time: 2022/7/2218:15
@Software: PyCharm
"""

from rest_framework import serializers, exceptions

from api_v1.models import User
from api_v1.utils import plugins


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate_password(self, value):
        return plugins.myhash(value)


class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(label="confirm_password")

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password"]

    def validate_confirm_password(self, value):
        if value != self.initial_data["password"]:
            raise exceptions.ValidationError("confirm_password error")
        return value

    def validate_password(self, value):
        return plugins.myhash(value)


class UserResetSerializer(UserSignupSerializer):
    class Meta:
        model = User
        fields = ["password", "confirm_password"]
