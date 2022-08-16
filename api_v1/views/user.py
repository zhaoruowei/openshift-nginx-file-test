# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: user.py
@Time: 2022/7/1823:31
@Software: PyCharm
"""

from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from api_v1.models import User, UserInfo, UserFollow
from api_v1.serializers.user import UserLoginSerializer, UserSignupSerializer, UserResetSerializer
from api_v1.utils.plugins import get_token
from api_v1.utils.auth import LoginAuthentication
from api_v1.utils.permission import OwnerPermission


class Index(APIView):
    """
    get
    url: /api/v1/
    return: {
        "code": 200,
        "msg": "Hello world!",
        "uid": null
    }
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ret = {"code": 200, "msg": "Hello world!", "uid": request.user}
        return Response(ret, status=200)
        pass


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    authentication_classes = []
    permission_classes = []

    @action(detail=True, methods=["post"])
    def refresh(self, request, *args, **kwargs):
        """
        check and refresh user token
        put
            url: /api/v1/user/refresh/
            header {
                "uid": 5,
                "Authorization": "Token 5bba4f47141e8f54c082e0d198fb14bad3c1353c09e94a18513b23e42b5f2b2a"
            }
            return {
                "code": 200,
                "msg": "refresh success!",
                "uid": 5,
                "Authorization": "Token 5bba4f47141e8f54c082e0d198fb14bad3c1353c09e94a18513b23e42b5f2b2a"
            }
        """
        ret = {"code": 200, "msg": "refresh success!"}
        # get request header
        token = request.META.get("HTTP_AUTHORIZATION")
        uid = request.META.get("HTTP_UID")
        # check redis for header token
        token_obj = cache.get(uid)

        if not token_obj or token_obj != token:
            ret["code"] = 400
            ret["msg"] = "token has expired"
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        else:
            # refresh cache expire time
            cache.touch(uid, 60 * 60 * 24 * 7)
            return Response(ret, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_name="login", url_path="login")
    def login(self, request, *args, **kwargs):
        """
        User Log in
        post
            url: /api/v1/user/login/
            data: {
                "username": "456",
                "password": "123"
            }
            return {
                "code": 200,
                "msg": "login success!",
                "uid": 5,
                "Authorization": "Token 5bba4f47141e8f54c082e0d198fb14bad3c1353c09e94a18513b23e42b5f2b2a"
            }
        """
        ret = {"code": 200, "msg": "login success!"}
        ser = UserLoginSerializer(data=request.data, many=False)
        if ser.is_valid():
            user = self.get_queryset()
            if user.filter(**ser.validated_data).exists():
                obj = user.filter(**ser.validated_data).first()
                user_token = get_token(str(obj.uid))
                cache.set(obj.uid, user_token, 60 * 60 * 24)
                ret["uid"] = obj.uid
                ret["Authorization"] = user_token
                return Response(ret, status=status.HTTP_200_OK)
            else:
                ret["code"] = 400
                ret["msg"] = "Username or Password error"
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        else:
            ret["code"] = 400
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_name="signup", url_path="signup",
            serializer_class=[UserSignupSerializer])
    def signup(self, request, *args, **kwargs):
        """
        user signup
        post
            url: /api/v1/user/signup/
            data: {
                "username": "456",
                "password": "123",
                "confirm_password"
            }
            return {
                "code": 200,
                "msg": "signup success!",
            }
        """
        ret = {"code": 201, "msg": "signup success!"}

        ser = UserSignupSerializer(data=request.data, many=False)
        if ser.is_valid():
            ser.validated_data.pop("confirm_password")
            obj = ser.save()
            UserInfo.objects.create(uid=obj)
            UserFollow.objects.create(uid=obj)
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            ret["code"] = 400
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)


class UserChangeView(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [LoginAuthentication, ]
    permission_classes = [OwnerPermission, ]

    def reset(self, request, *args, **kwargs):
        """
        reset password
        put
            url: /api/v1/user/<int:pk>/reset/
            header: {
                uid=pk
                Authorization=token
            }
            data: {
                "password": "456",
                "confirm_password": "456"
            }
            return {
                "code": 200,
                "msg": "reset success!",
            }
        """
        ret = {"code": 200, "msg": "reset success!"}
        ser = UserResetSerializer(data=request.data, many=False)
        if ser.is_valid():
            instance = self.get_object()
            ser.validated_data.pop("confirm_password")
            ser.update(instance=instance, validated_data=ser.validated_data)
            return Response(ret, status=status.HTTP_200_OK)
        else:
            ret["code"] = "400"
            ret["msg"] = ser.errors
            return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request, *args, **kwargs):
        """
        user logout
        post
            url: /api/v1/user/<int:pk>/logout/
            header: {
                uid=pk
                Authorization=token
            }
            return {
                "code": 200,
                "msg": "logout success!",
            }
        """
        ret = {"code": 204, "msg": "logout success!"}
        cache.delete(request.user)
        return Response(ret, status=status.HTTP_204_NO_CONTENT)
