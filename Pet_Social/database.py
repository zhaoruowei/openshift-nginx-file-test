# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: Pet_Social
@File: database.py.py
@Time: 2022/7/1823:01
@Software: PyCharm
"""

import os

from django.conf import settings

# 定义数据库引擎
engines = {
    "sqlite": "django.db.backends.sqlite3",
    "postgresql": "django.db.backends.postgresql_pycopg2",
    "mysql": "django.db.backends.mysql",
}


def config():
    service_name = os.getenv("DATABASE_SERVICE_NAME", "").upper().replace("-", "_")
    if service_name:
        engine = engines.get(os.getenv("DATABASE_ENGINE"), engines["sqlite"])
    else:
        engine = engines["sqlite"]
    name = os.getenv("DATABASE_NAME")
    if not name and engine == engines["sqlite"]:
        name = os.path.join(settings.BASE_DIR, "db,sqlite3")
    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name)),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name)),
    }
