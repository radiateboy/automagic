import MySQLdb

conn = MySQLdb.Connect(host='localhost', port=int(3306), user='root', passwd='root')
db = 'automatic'
cur = conn.cursor()
if not cur.execute("SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME='" + db + "'"):
    sql_create_db = "create database " + db + " DEFAULT CHARSET utf8 COLLATE utf8_general_ci"
    cur.execute(sql_create_db)
cur.close()
