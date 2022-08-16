# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: resource.py
@Time: 2022/7/2522:58
@Software: PyCharm
"""

from rest_framework import serializers

from api_v1.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    resource_id = serializers.IntegerField(source="rid", required=False)
    publisher_name = serializers.CharField(source="publisher.name", required=False)
    publisher = serializers.IntegerField(source="publisher.uid.uid", required=False)
    type = serializers.CharField(source="get_r_type_display", required=False)
    publisher_username = serializers.CharField(source="publisher.uid.username", required=False)
    release_time = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Resource
        exclude = ["rid"]

    def get_release_time(self, obj):
        ret = obj.release_time
        ret = ret.strftime("%Y-%m-%d %H:%M:%S")
        return ret
