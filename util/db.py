import pymysql

#插入函数
def dbexe(db,cursor,sql):
    try:
    # 执行sql语句
        cursor.execute(sql)
   # 提交到数据库执行
        db.commit()
    except pymysql.InternalError as e:
   # 如果发生错误则回滚
        db.rollback()

#查询函数
def dbsrh(db,cursor,sql):
    try:
    # 执行sql语句
        cursor.execute(sql)
   # 提交到数据库执行
        result=cursor.fetchall()
        return result
    except pymysql.InternalError as e:
        code, message = e.args
        print (">>>>>>>>>>>>>", code, message)
        return