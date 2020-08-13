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
                # print('hecheng', hecheng)
                books = json.dumps(bookmark['books'])
                print(books)
                # content = hecheng['content']
                # 一、插入合称表
                sql1 = 'insert into miniprogram_mergeinfo(title,flag) values("%s","%s")' % (
                    bookmark['name'], '史书典籍')
                self.conn.execute(sql1)
                self.conn.commit()
                sql2 = "update miniprogram_mergeinfo set data ='%s' where title == '%s';" % (books, bookmark['name'])
                self.conn.execute(sql2)
                self.conn.commit()
        self.conn.close()

    def select_data(self):
        cursor = self.conn.execute('select id,title,desc,data from miniprogram_mergeinfo')
        for row in cursor:
            print('id', row[0])
            print('title', row[1])
            print('desc', row[2])
            print('data', row[3], '\n')
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
    # mySql.select_data()
