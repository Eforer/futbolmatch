import pymysql

database = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='socialmatch',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )

