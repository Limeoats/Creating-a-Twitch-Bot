import pymysql.cursors

import cfg

def connect():
    connection = pymysql.connect(host=cfg.DBHOST,
                             user=cfg.DBUSER,
                             password=cfg.DBPASS,
                             db=cfg.DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def getCommands():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from BotCommands"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


