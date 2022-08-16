# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: petinfo.py
@Time: 2022/7/245:21
@Software: PyCharm
"""

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api_v1.models import PetInfo, UserInfo
from api_v1.serializers.petinfo import PetInfoSerializer
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission


class PetInfoView(ModelViewSet):
    queryset = PetInfo.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    serializer_class = [PetInfoSerializer]

    def list(self, request, *args, **kwargs):
        """
        get pet information
        get
            url: /api/v1/user/<int:pk>/pet/<int:pid>/, /api/v1/user/<int:pk>/pet/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "pet_gender_display": "Male",
                    "pet_name": "111",
                    "pet_avatar": null,
                    "pet_gender": 1,
                    "pet_age": 1,
                    "pet_type": "dog",
                    "master": 11
                },
            }
        """
        ret = {"code": 200, "msg": "success"}
        pid = kwargs.get("pid")
        obj = self.get_queryset()

        if pid:
            obj = obj.filter(pid=pid).first()
            many = False
        else:
            many = True

        if obj:
            ser = PetInfoSerializer(instance=obj, many=many)
            ret["data"] = ser.data
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret["code"] = 404
            ret["msg"] = "Not Found"
            return Response(ret, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """
        create pet information
        post
            url: /api/v1/user/<int:pk>/pet/
            header: {
                uid=pk
                Authorization=token
            }
            data {
                "pet_name": "json"
            }
            return {
                "code": 201,
                "msg": "success",
            }
        """
        ret = {"code": 201, "msg": "success"}
        user = UserInfo.objects.filter(uid=kwargs["pk"]).first()
        ser = PetInfoSerializer(data=request.data, many=False)
        if ser.is_valid():
            ser.save(master=user)
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            ret["code"] = "400"
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        update pet information
        put
            url: /api/v1/user/<int:pk>/pet/<int:pid>
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 201,
                "msg": "success",
            }
        """
        ret = {"code": 201, "msg": "success"}
        obj = self.get_queryset()
        pid = kwargs.get("pid")

        try:
            instance = obj.filter(pid=pid).first()
            request.data.setdefault("pet_name", instance.pet_name)

            ser = PetInfoSerializer(data=request.data, many=False)
            if ser.is_valid():
                ser.update(instance=instance, validated_data=ser.validated_data)
                return Response(ret, status=status.HTTP_201_CREATED)
            else:
                ret["code"] = 400
                ret["msg"] = ser.errors

                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        delete pet information
        delete
            url: /api/v1/user/<int:pk>/pet/<int:pid>/
            header: {
                uid=pk
                Authorization=token
            }
        """
        obj = self.get_queryset()
        pid = kwargs.get("pid")
        instance = obj.filter(pid=pid).first()
        if instance is not None:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
