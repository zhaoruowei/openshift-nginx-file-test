# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: comment.py
@Time: 2022/7/267:26
@Software: PyCharm
"""

from rest_framework import serializers

from api_v1.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source="cid", required=False)
    publisher_name = serializers.CharField(source="publisher.name", required=False)
    publisher = serializers.IntegerField(source="publisher.uid.uid", required=False)
    publisher_username = serializers.CharField(source="publisher.uid.username", required=False)
    parent_name = serializers.CharField(source="parent.title", required=False)
    parent = serializers.IntegerField(source="parent.rid", required=False)
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ["cid"]

    def get_create_time(self, obj):
        ret = obj.create_time
        ret = ret.strftime("%Y-%m-%d %H:%M:%S")
        return ret
