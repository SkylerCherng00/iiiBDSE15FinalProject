import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='ourAcc',
                             password='ourPW',
                             database='ourDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
