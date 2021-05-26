FROM ubuntu:18.04

MAINTAINER ray<tsbc@vip.qq.com>

LABEL version="2.0" by="ray" descriptio="python3.6 django 3.2.3"

ENV TZ=Asia/Shanghai
ENV PATH=/usr/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8


RUN mkdir /opt/automagic
WORKDIR /opt/automagic

RUN set -x;apt-get update \
&& apt-get install -y vim \
&& apt-get install -y tzdata \
&& apt-get install -y python3 \
&& apt-get install -y python3-pip \
&& pip3 install --upgrade pip 

COPY . /opt/automagic

RUN pip3 --no-cache-dir install -r /opt/automagic/requirements/base.txt \
     -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN pip3 --no-cache-dir install -r /opt/automagic/requirements/seleniumreq.txt \
     -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

ENTRYPOINT ["python3","start.py"]
