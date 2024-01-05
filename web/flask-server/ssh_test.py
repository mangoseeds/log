import pymysql
from sshtunnel import SSHTunnelForwarder


if __name__ == '__main__':
# SSH address mapping setup (not actually connects)
    with SSHTunnelForwarder(('222.107.147.71', 22),
                            ssh_username='user',
                            ssh_password='0000',
                            remote_bind_address=('127.0.0.1', 3306)
                           ) as tunnel:
        
# connect MySQL like local                           
        with pymysql.connect(
            host='127.0.0.1', #(local_host)
            user='root',
            passwd='Capstonlog33!',
            db='test_db',
            charset='utf8',
            port=tunnel.local_bind_port,
            cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = "select * from log_team"
                cur.execute(sql)
                print(sql)
                results = cur.fetchall()
                print(results)
                for result in results:
                    print(result)
