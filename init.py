import sqlite3
import os

'''
数据初始化
'''

__author__ = 'zhangyunan'

_data_path = 'data.db'

# 如果已经创建文件, 则直接删除
if os.path.exists(_data_path):
    os.remove(_data_path)


conn = sqlite3.connect(_data_path)
print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tb_database
       ( id INTEGER primary key autoincrement,
         name TEXT NOT NULL,
         host TEXT NOT NULL,
         port INT NOT NULL,
         user TEXT NOT NULL,
         password TEXT NOT NULL,
         status INT NOT NULL )''')
print("Table created successfully")
conn.commit()
conn.close()
