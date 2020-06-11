# 自动化测试平台 
## python3.8+   Django 3.0.6框架
>python3.8以下版本 使用Django 3.0.5 以上版本 ，django的 /admin/后台会异常退出，不使用/admin/后台不影响，安装请注意版本

### [新用户指导使用指南](https://github.com/radiateboy/automagic/wiki)

手动安装环境

> pip3 install -r requirements/base.txt

> pip3 install -r requirements/seleniumreq.txt

### Mysql/Mariadb 数据库 automatic/settings/common.py
```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',
        'NAME':'automatic',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}
```
#### 数据库初始化

```shell
python3 init_database.py

cd automagic

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py loaddata initial_data.json
```

另：内置关键字 在wiki #关键字创建# 页面（可以了解一下）

#### 创建管理员用户
```bash
python3 manage.py createsuperuser
```
按照提示进行输入要创建的用户名、邮箱、密码（8位以上，字母、字符、数字的组合）

#### 启动服务
```bash
python3 manage.py runserver 0.0.0.0:8000
```
_http://127.0.0.1:8000_   访问登录即可

## django admin 
http://127.0.0.1:8000/admin/

##如何执行测试脚本 
[点击查看如何执行测试](https://github.com/radiateboy/automagic/wiki/Seleniumkeyword%E4%BB%8B%E7%BB%8D)
## 公众号
扫一扫关注公众号

![开源优测](https://gitee.com/tsbc/automagic/raw/master/%E5%85%AC%E4%BC%97%E5%8F%B7.jpg)
