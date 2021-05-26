import pymysql
import os
from automatic.settings.common import MYSQL_HOST, MYSQL_PORT, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DBNAME

conn = pymysql.connect(host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD)
cur = conn.cursor()

if not cur.execute("SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME='" + MYSQL_DBNAME + "'"):
    print("创建数据库 [" + MYSQL_DBNAME + "]...")
    sql_create_db = "create database " + MYSQL_DBNAME + " DEFAULT CHARSET utf8 COLLATE utf8_general_ci"
    cur.execute(sql_create_db)
    print("创建数据库完成.")
    os.system("bash ./init.sh")
    print("导入关键字数据")
    sql_list = []
    with open('insertkeyword.sql', "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            sql_list.append(line)
    _con = pymysql.connect(host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD,
                           database=MYSQL_DBNAME, cursorclass=pymysql.cursors.DictCursor)
    with _con:
        with _con.cursor() as _cur:
            for sql in sql_list:
                try:
                    _cur.execute(sql)
                    print(sql)
                except:
                    _con.rollback()
            _con.commit()
        _cur.close()

cur.close()
print("service start ...")
os.system("python3 manage.py runserver 0.0.0.0:8000")
