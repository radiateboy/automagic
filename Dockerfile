FROM python:3.7-alpine3.10

LABEL version="1.0" by="taoyanli0808" description="请先配置数据库，然后执行docker build -f Dockerfile .构建镜像。"

WORKDIR /automagic

COPY . /automagic

RUN echo "http://mirrors.aliyun.com/alpine/v3.10/main/" > /etc/apk/repositories \
  && apk update --no-cache \
  && apk upgrade --no-cache \
  && apk add --no-cache build-base mariadb-dev libffi-dev \
  && sed -i '342a\unsigned int reconnect;' /usr/include/mysql/mysql.h \
  && pip --no-cache-dir install -r /automagic/requirements/base.txt \
     -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
  && pip --no-cache-dir install -r /automagic/requirements/seleniumreq.txt \
     -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

RUN python init_database.py \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@clover.cn', '52.clover')" | python manage.py shell

# 暴露出服务端口和MySQL端口
EXPOSE 3306 8000

CMD python manage.py runserver 0.0.0.0:8000
