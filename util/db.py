#import pymysql
import sqlite3

"""
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
"""


class DBProcer():
    def __init__(self,path_db:str) -> None:
        self.path_db=path_db

    def dbexe(self,sql_string:str) -> list:
        db=sqlite3.connect(database=self.path_db)
        cursor=db.cursor()
        cursor.execute(sql_string)
        db.commit()
        db.close()

    def create_table(self,table_name:str,cols:list):
        sql_string = f"""CREATE TABLE IF NOT EXISTS {table_name} ({cols[0]+" PRIMARY KEY,"+",".join(cols[1:])});"""
        self.dbexe(sql_string)

    def create_view(self,view_name:str,table_name:str,day:int,cols:list):
        cols_s=",".join(cols)
        sql_string=f"""CREATE VIEW IF NOT EXISTS {view_name} as select {cols_s} from (select * from {table_name} where (1674662400000-time)<{str(day*100000000)} order by time desc limit 100000) as v group by v.enemyname;"""
        self.dbexe(sql_string)

    def droper(self,type,name):
        sql_string=f"""DROP {type} IF EXISTS {name};"""
        self.dbexe(sql_string)
    
    def json2db(self,table_name,loader:list):
        cols=loader[0][0]
        self.cols=cols
        self.create_table(table_name=table_name,cols=cols)
        db=sqlite3.connect(database=self.path_db)
        cursor=db.cursor()
        for ld in loader:
            format_v=','.join(['?'] * len(cols))
            sql_string = f"""INSERT INTO {table_name} ({",".join(cols)}) VALUES ({format_v} ) ON conflict({cols[0]})  DO NOTHING;""" 
            cursor.executemany(sql_string, loader[0][1:])
        db.commit()
        db.close()