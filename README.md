# 自动化测试平台 
## python3.6+   Django 3.0.6框架

### [新用户指导使用指南](https://github.com/radiateboy/automagic/wiki)

手动安装环境

> pip install -r requirements/base.txt

> pip install -r requirements/seleniumreq.txt

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
python init_database.py

cd automagic

python manage.py makemigrations

python manage.py migrate
```
_初始化会报createSuperuser的错误，此处忽略即可，下面会用命令创建用户。_

另：内置关键字 在wiki #关键字创建# 页面（可以了解一下）

#### 创建管理员用户
```bash
python manage.py createsuperuser
```
按照提示进行输入要创建的用户名、邮箱、密码（8位以上，字母、字符、数字的组合）

#### 启动服务
```bash
manage.py runserver 0.0.0.0:8000
```
_http://127.0.0.1:8000_   访问登录即可

## django admin 
http://127.0.0.1:8000/admin/


## 公众号
扫一扫关注公众号

![开源优测](公众号.jpg)
