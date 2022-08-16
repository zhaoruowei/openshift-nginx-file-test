# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: userinfo.py
@Time: 2022/7/2317:07
@Software: PyCharm
"""

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api_v1.models import UserInfo
from api_v1.serializers.userinfo import UserInfoSerializer
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission


class UserInfoView(ModelViewSet):
    queryset = UserInfo.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    serializer_class = [UserInfoSerializer]

    def list(self, request, *args, **kwargs):
        """
        get user information
        get
            url: /api/v1/userinfo/<int:pk>/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "user_id": 11,
                    "gender_display": "Male",
                    "name": "hala",
                    "avatar": null,
                    "gender": 1,
                    "age": 18,
                    "email": "123@123.com",
                    "phone": "123",
                    "join_time": "2022-07-23"
                }
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = self.get_object()

        if obj:
            ser = UserInfoSerializer(instance=obj, many=False)
            ret["data"] = ser.data
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret["code"] = 404
            ret["msg"] = "Not Found"
            return Response(ret, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        """
        put for update
        put
            url: /api/v1/userinfo/<int:pk>/
            header: {
                uid=pk
                Authorization=token
            }
            data: {
                "name": "hala",
                "gender": 1,
                "age": 18,
                "email": "123@123.com",
                "phone": "123"
            }
            return {
                "code": 200,
                "msg": "success!",
            }
        """
        ret = {"code": 200, "msg": "success"}

        ser = UserInfoSerializer(data=request.data, many=False)
        if ser.is_valid():
            instance = self.get_object()
            ser.update(instance=instance, validated_data=ser.validated_data)
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret["code"] = 400
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
