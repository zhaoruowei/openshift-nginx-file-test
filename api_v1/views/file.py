# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: file.py
@Time: 2022/7/2322:59
@Software: PyCharm
"""

import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission
from api_v1.models import UserInfo, PetInfo, Resource

# re_path(r'upload/(?P<pk>\d+)/resource/(?P<rid>\d+)/(?P<filename>[^/]+)/$'
class FileUploadView(APIView):
    """
    upload file
    post
        url:
            upload/(?P<pk>\d+)/resource/(?P<rid>\d+)/(?P<filename>[^/]+)/$
            /api/v1/upload/11/resource/1/test.png/
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
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        obj = Resource.objects.filter(rid=kwargs["rid"], publisher_id=kwargs["pk"])
        folder = os.path.join(os.getenv('SHARE_PATH'), 'resource', 'user_{}'.format(kwargs.get("pk")))
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = 'resource_{}.'.format(kwargs.get("rid")) + kwargs.get("filename").split(".")[-1]
        path = os.path.join(folder, filename)
        print(path)
        with open(path, "wb+") as PNG:
            for chunk in file_obj.chunks():
                PNG.write(chunk)
        obj.update(media=path)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvatarUploadView(ModelViewSet):
    """
    upload file
    put
        url: /api/v1/upload/(?P<pk>\d+)/(?P<filename>[^/]+)/$, /api/v1/upload/(?P<pk>\d+)/pet/(?P<pid>\d+)/(?P<filename>[^/]+)/$
            http://127.0.0.1:8000/api/v1/upload/11/test.png/, http://127.0.0.1:8000/api/v1/upload/11/pet/2/test.png/
        header: {
            uid=pk
            Authorization=token
        }
        data {
            file, png
        }
    """
    queryset = UserInfo.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    parser_classes = [FileUploadParser]

    def update(self, request, *args, **kwargs):
        file_obj = request.data['file']
        instance = self.get_queryset()
        instance = instance.filter(uid=kwargs.get("pk"))

        folder = os.path.join(os.getenv('SHARE_PATH'), 'avatar', 'user_{}'.format(kwargs.get("pk")))
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not kwargs.get("pid"):
            filename = 'user_{}.'.format(kwargs.get("pk")) + kwargs.get("filename").split(".")[-1]
        else:
            filename = 'user_{}_pet_{}.'.format(kwargs.get("pk"), kwargs.get("pid")) + \
                       kwargs.get("filename").split(".")[-1]
            instance = instance.first()
            instance = PetInfo.objects.filter(master=instance, pid=kwargs.get("pid"))

        path = os.path.join(folder, filename)
        with open(path, "wb+") as PNG:
            for chunk in file_obj.chunks():
                PNG.write(chunk)

        if not kwargs.get("pid"):
            instance.update(avatar=path)
        else:
            instance.update(pet_avatar=path)
        return Response(status=status.HTTP_204_NO_CONTENT)
