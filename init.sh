#!/bin/bash
set -e

echo '生成Django表结构....'
python3 manage.py makemigrations
echo 'Django表结构更新完成.'

echo '创建表结构....'
python3 manage.py migrate
echo '表结构创建完成.'

echo '创建Django超级用户'
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@automagic.cn', 'admin@123')" | python3 manage.py shell
echo '创建超级用户admin，密码：admin@123 完成'
