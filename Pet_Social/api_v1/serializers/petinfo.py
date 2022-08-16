# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: petinfo.py
@Time: 2022/7/247:28
@Software: PyCharm
"""

from rest_framework import serializers

from api_v1.models import PetInfo


class PetInfoSerializer(serializers.ModelSerializer):
    pet_gender_display = serializers.CharField(source="get_pet_gender_display", required=False)
    master_id = serializers.CharField(source="master.uid.uid", required=False)
    pet_id = serializers.IntegerField(source="pid", required=False)

    class Meta:
        model = PetInfo
        exclude = ["pid", "master"]
