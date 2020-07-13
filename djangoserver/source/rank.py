import json
import sqlite3


# 插入诗词内容工具类
class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        with open('rank.json', 'r', encoding='utf-8') as load_f:
            rank = json.load(load_f)
            for rankObj in rank:
                # print('line', line)
                # 一、插入诗词分类和标识对应表
                sql1 = 'insert into miniprogram_poetryflag(poetry_type) values("%s")' % ('诗词排行榜')
                self.conn.execute(sql1)
                # 获取插入数据库的标识
                sql1_result = self.conn.execute(
                    "select * from miniprogram_poetryflag where poetry_type=:name", {"name": '诗词排行榜'})
                sql1_result_index = sql1_result.fetchone()[0]
                print(sql1, sql1_result.fetchone(), sql1_result_index)
                self.conn.commit()
                for poetryObj in rankObj['poetrys']:
                    sql3 = 'insert into miniprogram_poetry(poetry_flag,mark_index,title,time,author,content,pic) values(%d,%d,"%s","%s","%s","%s","%s")' % (
                        sql1_result_index, int(poetryObj['index']), poetryObj['title'], poetryObj['time'],
                        poetryObj['author'], poetryObj['content'], poetryObj['pic'])
                    self.conn.execute(sql3)
                    self.conn.commit()
                    print(sql3)
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
