import json
import sqlite3


# 插入诗词内容工具类
class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        with open('oldbook.json', 'r', encoding='utf-8') as load_f:
            data = json.load(load_f)
            for bookmark in data['bookmarks']:
                print(bookmark['name'])
                # 一、插入合称表
                sql1 = "update miniprogram_mergeinfo set desc ='%s' where title = '%s';" % (
                    bookmark['desc'], bookmark['name'])
                self.conn.execute(sql1)
                self.conn.commit()
                print(sql1)
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
