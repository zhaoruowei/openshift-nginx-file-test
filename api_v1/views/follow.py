# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: follow.py
@Time: 2022/7/243:28
@Software: PyCharm
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from api_v1.models import UserInfo, User, UserFollow, UserFollowed
from api_v1.serializers.userinfo import UserInfoSerializer
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission


class FollowUserView(ModelViewSet):
    authentication_classes = [LoginAuthentication, ]
    permission_classes = [OwnerPermission, ]

    def follow_list(self, request, *args, **kwargs):
        """
        get all follow user
        get
            url: /api/v1/user/<int:pk>/follow/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "user_id": 14,
                        "gender_display": null,
                        "name": null,
                        "avatar": null,
                        "gender": null,
                        "age": null,
                        "email": null,
                        "phone": null,
                        "join_time": "2022-07-24"
                    },
                ]
            }
        """
        ret = {"code": 200, "msg": "success"}
        obj = User.objects.filter(uid=kwargs.get("pk")).first()
        follow_list = UserFollow(uid=obj).follow.all().order_by("uid")
        info_list = [UserInfo.objects.filter(uid=item).first() for item in follow_list]
        ser = UserInfoSerializer(instance=info_list, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def followed_list(self, request, *args, **kwargs):
        """
        get all followed user
        get
            url: /api/v1/user/<int:pk>/followed/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "user_id": 14,
                        "gender_display": null,
                        "name": null,
                        "avatar": null,
                        "gender": null,
                        "age": null,
                        "email": null,
                        "phone": null,
                        "join_time": "2022-07-24"
                    },
                ]
            }
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=obj, request=request, view=self)
        ser = ResourceSerializer(instance=pager_obj, many=True)
        """
        ret = {"code": 200, "msg": "success"}
        obj = User.objects.filter(uid=kwargs.get("pk")).first()
        followed_list = UserFollowed(uid=obj).followed_by.all()
        pg = PageNumberPagination()
        pager_obj = pg.paginate_queryset(queryset=followed_list, request=request, view=self)
        info_list = [UserInfo.objects.filter(uid=item).first() for item in pager_obj]
        ser = UserInfoSerializer(instance=info_list, many=True)
        ret["data"] = ser.data
        return Response(ret, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        post new follow user
        post
            url: /api/v1/user/<int:pk>/follow/<int:person>/
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
        if kwargs.get("pk") == kwargs.get("person"):
            ret["code"] = 400
            ret["msg"] = "wrong params"
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

        obj = User.objects.filter(uid=kwargs.get("pk")).first()
        follow = User.objects.filter(uid=kwargs.get("person")).first()
        # follow list
        user_follow = UserFollow(uid=obj)
        user_follow.save()
        user_follow.follow.add(follow)

        # followed list
        user_followed = UserFollowed(uid=follow)
        user_followed.save()
        user_followed.followed_by.add(obj)
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        delete follow user
        post
            url: /api/v1/user/<int:pk>/follow/<int:person>/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "success",
            }
        """
        user_follow = UserFollow(uid=User.objects.filter(uid=kwargs["pk"]).first())
        follow = User(uid=kwargs["person"])
        user_follow.follow.remove(follow)

        user_followed = UserFollowed(uid=User.objects.filter(uid=kwargs["person"]).first())
        followed = User(uid=kwargs["pk"])
        user_followed.followed_by.remove(followed)

        return Response(status=status.HTTP_204_NO_CONTENT)



        # # follow list
        #
        # user_follow.save()
        # user_follow.follow.add(follow)
        #
        # # followed list
        # user_followed = UserFollowed(uid=follow)
        # user_followed.save()
        # user_followed.followed_by.add(obj)
        # return Response(ret, status=status.HTTP_200_OK)