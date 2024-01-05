import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='Capstonlog33!', db='test_db', charset='utf8')

cursor = db.cursor()

sql = "select * from log_team"

cursor.execute(sql)

print(cursor.fetchall())

db.close()