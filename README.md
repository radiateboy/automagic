# 自动化测试平台 
## python2.7 Django 1.10框架
### Mysql 数据库 automated/settings.py
```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',
        'NAME':'autoplat',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}
```
#### runserver
```manage.py runserver 0.0.0.0:8000```

