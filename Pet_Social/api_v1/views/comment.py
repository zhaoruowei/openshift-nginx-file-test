# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: comment.py
@Time: 2022/7/267:13
@Software: PyCharm
"""

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from api_v1.models import Comment, UserInfo, Resource
from api_v1.serializers.comment import CommentSerializer
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission

"""
    path('user/<int:pk>/comment/', comment.CommentView.as_view({'get': 'user_list'})),
    path('resource/<int:pk>/comment/', comment.CommentView.as_view({'get': 'resource_list', 'post': 'create'})),
    path('resource/<int:pk>/comment/<int:cid>/', comment.CommentView.as_view({'get': 'view_one', 'delete': 'destroy'})),
    视图类与权限的问题，序列化完善
"""


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    authentication_classes = []
    permission_classes = []
    serializer_class = [CommentSerializer]

    def resource_list(self, request, *args, **kwargs):
        """
        get resource all comment
        get
            url: /api/v1/resource/<int:pk>/comment/
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "comment_id": 1,
                        "publisher_name": "hala",
                        "publisher": 11,
                        "parent_name": "test11",
                        "parent": 1,
                        "create_time": "2022-07-27 00:49:50",
                        "content": "test"
                    }
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}

        obj = self.get_queryset().filter(parent_id=kwargs["pk"]).order_by("-create_time")
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=obj, request=request, view=self)
        ser = CommentSerializer(instance=pager_obj, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)


class CommentUserView(ModelViewSet):
    queryset = Comment.objects.all()
    authentication_classes = [LoginAuthentication]
    permission_classes = [OwnerPermission]
    serializer_class = [CommentSerializer]

    def user_list(self, request, *args, **kwargs):
        """
        get user all comment
        get
            url: /api/v1/user/<int:pk>/comment/
            header {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "comment_id": 1,
                        "publisher_name": "hala",
                        "publisher": 11,
                        "parent_name": "test11",
                        "parent": 1,
                        "create_time": "2022-07-27 00:49:50",
                        "content": "test"
                    },
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = self.get_queryset()
        obj = obj.filter(publisher_id=kwargs["pk"]).order_by("-create_time")
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=obj, request=request, view=self)
        ser = CommentSerializer(instance=pager_obj, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        post new comment for a resource
        post
            url: /api/v1/user/<int:pk>/resource/<int:rid>/comment/
            header {
                uid=pk
                Authorization=token
            }
            body {
                "content": "test"
            }
            return {
                "code": 201,
                "msg": "success",
            }
        """
        ret = {"code": 201, "msg": "success"}
        try:
            user = UserInfo.objects.filter(uid=request.user).first()
            res = Resource.objects.filter(rid=kwargs["rid"]).first()
            com = Comment.objects.filter(parent=res)
            ser = CommentSerializer(data=request.data, many=False)
            if ser.is_valid():
                ser.save(publisher=user, parent=res)
                Resource.objects.filter(rid=kwargs["rid"]).update(comments_count=com.count())
                return Response(ret, status=status.HTTP_201_CREATED)
            else:
                ret["code"] = 400
                ret["msg"] = ser.errors
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods='GET', detail=True)
    def view_one(self, request, *args, **kwargs):
        """
        get a comment
        get
            url: /api/v1/user/<int:pk>/resource/<int:rid>/comment/<int:cid>/
            header {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "comment_id": 4,
                    "publisher_name": "hala",
                    "publisher": 11,
                    "parent_name": "test11",
                    "parent": 1,
                    "create_time": "2022-07-27 00:21:17",
                    "content": "test"
                }
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = self.get_queryset()
        obj = obj.filter(parent_id=kwargs["rid"], cid=kwargs["cid"]).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = CommentSerializer(instance=obj, many=False)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        delete a comment
        delete
            url: /api/v1/user/<int:pk>/resource/<int:rid>/comment/<int:cid>/
            header {
                uid=pk
                Authorization=token
            }
        """
        obj = self.get_queryset()
        obj = obj.filter(parent_id=kwargs["rid"], cid=kwargs["cid"]).first()
        if obj is not None:
            obj.delete()
            com = Comment.objects.filter(parent_id=kwargs["rid"])
            Resource.objects.filter(rid=kwargs["rid"]).update(comments_count=com.count())
        return Response(status=status.HTTP_204_NO_CONTENT)
        pass
