#!/bin/bash

# 启动django服务
python3 manage.py runserver 0.0.0.0:8000 >~/django.log 2>&1 &
echo $! > ~/django.pid