#! /bin/bash

python manage.py makemigrations
python manage.py migrate
mkdir media
uwsgi --ini uwsgi.ini
