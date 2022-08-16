# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: resource.py
@Time: 2022/7/2522:56
@Software: PyCharm
"""

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from api_v1.models import Resource, UserInfo, ResourceLike, UserFollow
from api_v1.serializers.resource import ResourceSerializer
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission


class ResourceView(ModelViewSet):
    queryset = Resource.objects.all()
    authentication_classes = []
    permission_classes = []
    serializer_class = [ResourceSerializer]
    throttle_classes = []

    def list(self, request, *args, **kwargs):
        """
        get all resource
        get
            url: /api/v1/resource/
            header: {
            }
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "resource_id": 1,
                        "publisher_name": "hala",
                        "publisher": 11,
                        "r_type": "article",
                        "title": "111",
                        "views_count": 0,
                        "comments_count": 0,
                        "likes_count": 0,
                        "content": "111111111111",
                        "media": null,
                        "release_time": "2022-07-25 23:34:40"
                    },
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = self.get_queryset().order_by("-release_time")
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=obj, request=request, view=self)
        ser = ResourceSerializer(instance=pager_obj, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    @action(methods="GET", detail=True)
    def view_one(self, request, *args, **kwargs):
        """
        get one resource
        get
            url: /api/v1/resource/<int:rid>
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "resource_id": 1,
                    "publisher_name": "hala",
                    "publisher": 11,
                    "r_type": "article",
                    "title": "111",
                    "views_count": 0,
                    "comments_count": 0,
                    "likes_count": 0,
                    "content": "111111111111",
                    "media": null,
                    "release_time": "2022-07-25 23:34:40"
                }
                "like_flag": 1,
                "user_follow_flag": 1,
            }
        """
        ret = {"code": 200, "msg": "success", "like_flag": 0, "user_follow_flag": -1}
        self.lookup_field = "rid"
        obj = self.get_object()
        if int(request.META.get("HTTP_UID")) != obj.publisher_id:
            Resource.objects.filter(rid=kwargs["rid"]).update(views_count=obj.views_count + 1)
            obj.views_count += 1
        ser = ResourceSerializer(instance=obj, many=False)
        ret["data"] = ser.data

        uid = request.META.get("HTTP_UID")
        publisher = obj.publisher_id
        user_follow_flag = int(UserFollow.objects.filter(uid=uid, follow=publisher).exists())
        if int(uid) == int(publisher):
            user_follow_flag = -1
        like_flag = int(ResourceLike.objects.filter(uid=uid, like=kwargs["rid"]).exists())
        ret["like_flag"] = like_flag
        ret["user_follow_flag"] = user_follow_flag
        return Response(ret, status=status.HTTP_200_OK)


class ResourceChangeView(ModelViewSet):
    queryset = Resource.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    serializer_class = [ResourceSerializer]

    def list(self, request, *args, **kwargs):
        """
        get user all resource
        get
            url: user/<int:pk>/resource/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 201,
                "msg": "success",
                "data": [
                    {
                        "resource_id": 1,
                        "publisher_name": "hala",
                        "publisher": 11,
                        "r_type": "article",
                        "title": "111",
                        "views_count": 0,
                        "comments_count": 0,
                        "likes_count": 0,
                        "content": "111111111111",
                        "media": null,
                        "release_time": "2022-07-25 23:34:40"
                    },
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = self.get_queryset().order_by("-release_time")
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=obj, request=request, view=self)
        ser = ResourceSerializer(instance=pager_obj, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        create resource
        post
            url: /api/v1/user/<int:pk>/resource/
            header: {
                uid=pk
                Authorization=token
            }
            data {
                "title": "test",
                "r_type": 1
            }
            return {
                "code": 201,
                "msg": "success",
            }
        """
        ret = {"code": 201, "msg": "success"}
        user = UserInfo.objects.filter(uid=kwargs["pk"]).first()
        ser = ResourceSerializer(data=request.data, many=False)
        if ser.is_valid():
            obj = ser.save(publisher=user)
            ret["rid"] = obj.rid
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            ret["code"] = 400
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        update resource
        put
            url: /api/v1/user/<int:pk>/resource/<int:rid>/
            header: {
                uid=pk
                Authorization=token
            }
            data {
                "title": "test",
                "r_type": 1
            }
            return {
                "code": 201,
                "msg": "success",
            }
        """
        ret = {"code": 201, "msg": "success"}
        obj = self.get_queryset()
        rid = kwargs.get("rid")
        try:
            instance = obj.filter(rid=rid).first()
            ser = ResourceSerializer(data=request.data, many=False)
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
        delete resource
        delete
            url: /api/v1/user/<int:pk>/resource/<int:pid>/
            header: {
                uid=pk
                Authorization=token
            }
        """
        obj = self.get_queryset()
        rid = kwargs.get("rid")
        instance = obj.filter(rid=rid).first()
        if instance is not None:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceLikeView(ModelViewSet):
    queryset = Resource.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    serializer_class = [ResourceSerializer]

    def list(self, request, *args, **kwargs):
        """
        get user all like resource
        get
            url: /api/v1/user/<int:pk>/like/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "resource_id": 1,
                        "publisher_name": "hala",
                        "publisher": 11,
                        "type": "article",
                        "release_time": "2022-07-25 23:34:40",
                        "title": "test11",
                        "r_type": 1,
                        "views_count": 4,
                        "comments_count": 0,
                        "likes_count": 0,
                        "content": "111111111111",
                        "media": null
                    }
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = UserInfo.objects.filter(uid=kwargs.get("pk")).first()
        like_list = ResourceLike(uid=obj).like.all().order_by("-release_time")
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=like_list, request=request, view=self)
        ser = ResourceSerializer(instance=pager_obj, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        post new like resource
        post
            url: /api/v1/user/<int:pk>/like/<int:rid>/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
            }
        """
        ret = {"code": 200, "msg": "success"}

        obj = UserInfo.objects.filter(uid=kwargs.get("pk")).first()
        res = Resource.objects.filter(rid=kwargs.get("rid"))
        if obj is None or res is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # like list
        user_follow = ResourceLike(uid=obj)
        user_follow.save()
        user_follow.like.add(res.first())
        # add resource like count
        res.update(likes_count=ResourceLike.objects.filter(like=res.first()).count())
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        cancel like resource
        delete
            url: /api/v1/user/<int:pk>/like/<int:rid>/
            header: {
                uid=pk
                Authorization=token
            }
        """
        user = UserInfo.objects.filter(uid=kwargs["pk"]).first()
        obj = ResourceLike(uid=user)
        res = Resource(rid=kwargs["rid"])
        if obj and res:
            obj.like.remove(res)
            Resource.objects.filter(rid=kwargs["rid"]).update(likes_count=ResourceLike.objects.filter(like=res).count())
        return Response(status=status.HTTP_204_NO_CONTENT)
