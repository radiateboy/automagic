# 由于社区更新，requirements.txt必须显示生名django-model-utils==3.2.0；
# scapy建议采用2.4.3版本来规避编译问题，构建前不要忘记修改settings的数据库配置哦！

FROM python:2.7-alpine3.10

MAINTAINER taoyanli0808

WORKDIR /automagic

COPY . /automagic

RUN echo "http://mirrors.aliyun.com/alpine/v3.10/main/" > /etc/apk/repositories \
  && apk update --no-cache \
  && apk upgrade --no-cache \
  && apk add --no-cache build-base mariadb-dev libffi-dev \
  && sed -i '342a\unsigned int reconnect;' /usr/include/mysql/mysql.h \
  && pip --no-cache-dir install -r /automagic/requirements.txt \
     -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

 RUN python setup.py install \
  && python manage.py makemigrations \
  && python manage.py migrate \
  || echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@clover.com', '52.clover')" | python manage.py shell

# 暴露出服务端口和MySQL端口
EXPOSE 3306 8000

CMD python manage.py runserver 0.0.0.0:8000
