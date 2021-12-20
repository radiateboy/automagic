# 自动化测试平台 
## python3.8+   Django 3.2.10框架
>python3.8以下版本 使用Django 3.0.5 以上版本 ，django的 /admin/后台会异常退出，不使用/admin/后台不影响，安装请注意版本

### [新用户指导使用指南](https://github.com/radiateboy/automagic/wiki)

# (一)源码安装
> pip3 install -r requirements/base.txt
>
> pip3 install -r requirements/seleniumreq.txt

### Mysql/Mariadb 数据库 automatic/settings/common.py
```python
MYSQL_USERNAME =  os.environ.get('MYSQL_USERNAME', 'root')
MYSQL_PASSWORD =  os.environ.get('MYSQL_PASSWORD', '123456')
MYSQL_HOST =  os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_PORT =  os.environ.get('MYSQL_PORT', '3306')
MYSQL_DBNAME =  os.environ.get('MYSQL_DBNAME', 'automatic')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DBNAME,
        'USER': MYSQL_USERNAME,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
    }
}
```
#### 初始化并启动服务

```shell
python3 start.py
```

另：内置关键字 在wiki #关键字创建# 页面（可以了解一下）

_http://127.0.0.1:8000_   访问登录即可

默认管理员用户：admin， 密码：admin@123 
# (二)docker安装
## 方法一: 命令安装启动
```shell script
docker pull tsbc520/automagic:2.0
```
启动docker容器：
```shell script
docker run -d -p 8000:8000 \
-e MYSQL_HOST=192.168.10.167 \
-e MYSQL_PORT=3306 \
-e MYSQL_DBNAME=automatic \
-e MYSQL_USERNAME=root \
-e MYSQL_PASSWORD=123456 \
tsbc520/automagic:2.0 
```

## 方法二: docker-compose
```shell script
docker-compose up
```

## 如何执行测试脚本 
[点击查看如何执行测试](https://github.com/radiateboy/automagic/wiki/Seleniumkeyword%E4%BB%8B%E7%BB%8D)
## 公众号
扫一扫关注公众号

![开源优测](https://gitee.com/tsbc/automagic/raw/master/%E5%85%AC%E4%BC%97%E5%8F%B7.jpg)
