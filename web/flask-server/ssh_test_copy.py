import pymysql
from sshtunnel import SSHTunnelForwarder

tunnel = SSHTunnelForwarder(('222.107.147.71', 22), ssh_username='user', ssh_password='0000', remote_bind_address=('127.0.0.1', 3306))
tunnel.start()

db = pymysql.connect(host='127.0.0.1', user='root', passwd='Capstonlog33!', db='test_db', charset='utf8', port=tunnel.local_bind_port, cursorclass=pymysql.cursors.DictCursor)
cur = db.cursor()

sql = "select * from log_team"
cur.execute(sql)
results = cur.fetchall()
print(results)

for result in results:
    print(result)