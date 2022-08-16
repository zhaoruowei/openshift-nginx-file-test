# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: urls.py
@Time: 2022/7/2216:59
@Software: PyCharm
"""

from django.urls import path, re_path

from api_v1.views import user, userinfo, file, follow, pet, resource, comment

urlpatterns = [
    path('', user.Index.as_view()),
    # login, signup
    path('user/login/', user.UserView.as_view({'post': 'login'})),  #
    path('user/signup/', user.UserView.as_view({'post': 'signup'})),  #
    path('user/refresh/', user.UserView.as_view({'post': 'refresh'})),  #

    # logout, reset password
    path('user/<int:pk>/reset/', user.UserChangeView.as_view({'put': 'reset'})),  #
    path('user/<int:pk>/logout/', user.UserChangeView.as_view({'post': 'logout'})),  #

    # modify personal info
    path('userinfo/<int:pk>/', userinfo.UserInfoView.as_view({'get': 'list', 'put': 'update'})),  #

    # follow/followed management
    path('user/<int:pk>/follow/', follow.FollowUserView.as_view({'get': 'follow_list'})), ##
    path('user/<int:pk>/follow/<int:person>/', follow.FollowUserView.as_view({'post': 'create', 'delete': "destroy"})),
    path('user/<int:pk>/followed/', follow.FollowUserView.as_view({'get': 'followed_list'})),

    # pet management
    path('user/<int:pk>/pet/', pet.PetInfoView.as_view({'get': 'list', 'post': 'create'})),  #
    path('user/<int:pk>/pet/<int:pid>/',
         pet.PetInfoView.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy'})),  #

    # avatar upload(http://127.0.0.1:8000/api/v1/upload/11/test.png/)
    re_path(r'upload/(?P<pk>\d+)/(?P<filename>[^/]+)/$', file.AvatarUploadView.as_view({'put': 'update'})),
    re_path(r'upload/(?P<pk>\d+)/pet/(?P<pid>\d+)/(?P<filename>[^/]+)/$',
            file.AvatarUploadView.as_view({'put': 'update'})),

    # resource management
    path('resource/', resource.ResourceView.as_view({'get': 'list', 'post': 'create'})),  ## get
    path('resource/<int:rid>/',
         resource.ResourceView.as_view({'get': 'view_one', 'put': 'update', 'delete': 'destroy'})),
    path('user/<int:pk>/resource/', resource.ResourceChangeView.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>/resource/<int:rid>/',
         resource.ResourceChangeView.as_view({'put': 'update', 'delete': 'destroy'})),

    # resource like
    path('user/<int:pk>/like/', resource.ResourceLikeView.as_view({'get': 'list'})),  #
    path('user/<int:pk>/like/<int:rid>/', resource.ResourceLikeView.as_view({'post': 'create', 'delete': 'destroy'})),  #

    # comment management
    path('resource/<int:pk>/comment/', comment.CommentView.as_view({'get': 'resource_list'})),
    path('user/<int:pk>/comment/', comment.CommentUserView.as_view({'get': 'user_list'})),
    path('user/<int:pk>/resource/<int:rid>/comment/', comment.CommentUserView.as_view({'post': 'create'})),
    path('user/<int:pk>/resource/<int:rid>/comment/<int:cid>/',
         comment.CommentUserView.as_view({'get': 'view_one', 'delete': 'destroy'})),

    # resource file upload
    re_path(r'upload/(?P<pk>\d+)/resource/(?P<rid>\d+)/(?P<filename>[^/]+)/$', file.FileUploadView.as_view()),
]
