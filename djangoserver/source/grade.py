import json
import sqlite3


class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        with open('grade.json', 'r', encoding='utf-8') as load_f:
            data = json.load(load_f)
            for line in data:
                print('line', line)
                sql = 'insert into miniprogram_poetry(type,title,image,poetrys) values("%s","%s","%s","%s")' % (
                    "课本古诗", line['grade'], line['image'], line['poetrys'])
                print('sql', sql)
                self.conn.execute(sql)
                self.conn.commit()
        self.conn.close()

    def select_data(self):
        cursor = self.conn.execute('select id,type,title,image,poetrys from miniprogram_poetry')
        for row in cursor:
            print('id', row[0])
            print('type', row[1])
            print('title', row[2])
            print('image', row[3])
            print('poetrys', row[4], '\n')
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
    # mySql.select_data()
