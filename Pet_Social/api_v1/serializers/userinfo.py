# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: userinfo.py
@Time: 2022/7/2317:45
@Software: PyCharm
"""

from rest_framework import serializers

from api_v1.models import UserInfo, UserFollow, UserFollowed


class UserInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="uid_id", required=False)
    username = serializers.CharField(source="uid.username", required=False)
    gender_display = serializers.CharField(source="get_gender_display", required=False)
    following = serializers.SerializerMethodField(required=False)
    followed = serializers.SerializerMethodField(required=False)

    class Meta:
        model = UserInfo
        exclude = ["uid"]

    def validate_gender(self, value):
        return value

    def get_following(self, obj):
        follow = UserFollow(uid=obj.uid)
        count = follow.follow.count()
        return count

    def get_followed(self, obj):
        followed = UserFollowed(uid=obj.uid)
        count = followed.followed_by.count()
        return count
