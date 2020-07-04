# -*- coding: utf-8 -*-
"""
Proj: my_plotly
Created on:   2020/6/10 10:51
@Author: RAMSEY

"""
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
    'user', '', 'wuhan.yibai-it.com', 33061, 'team_station', 'utf8'))


# 数据库类型:mysql
# 数据库驱动选择:pymysql
# 数据库用户名:user
# 用户密码:password
# 服务器地址:wuhan.yibai-it.com
# 端口: 33061
# 数据库: team_station


def detect_db_conn(func):
    def wrapper(*args, **kwargs):
        try:
            conn = engine.connect()
            conn.close()
        except:
            raise ConnectionError('CAN NOT CONNECT MYSQL:ip:wuhan.yibai-it.com db:team_station')
        return func(*args, **kwargs)

    return wrapper


@detect_db_conn
def read_table(sql):
    # 执行sql
    conn = engine.connect()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# If table exists, do nothing.
@detect_db_conn
def to_sql(df, table):
    # 执行sql
    conn = engine.connect()
    try:
        df.to_sql(table, conn, if_exists='fail', index=False)
    except:
        conn.rollback()


#  If table exists, drop it, recreate it, and insert data.
@detect_db_conn
def to_sql_replace(df, table):
    # 执行sql
    conn = engine.connect()
    try:
        df.to_sql(table, conn, if_exists='replace', index=False)
    except:
        conn.rollback()


# If table exists, insert data. Create if does not exist.
@detect_db_conn
def to_sql_append(df, table):
    # 执行sql
    conn = engine.connect()
    try:
        df.to_sql(table, conn, if_exists='append', index=False)
    except:
        conn.rollback()


if __name__ == "__main__":
    sql = "SELECT * FROM only_station_info"
    df1 = read_table(sql)
    df2 = read_table(sql)
    print(df1)
    print(df2)
