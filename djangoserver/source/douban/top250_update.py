# 插入诗词内容工具类
import json
import sqlite3


class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        with open('电影TOP250.json', 'r', encoding='utf-8') as load_f:
            movies = json.load(load_f)
            for movieObj in movies:
                subject = movieObj['subject']
                movie_index = int(movieObj['index'])
                print('line', movie_index, movieObj['title'])
                # 一、更新电影数据表数据
                sql1 = "update miniprogram_movie set subject ='%s' where movie_index = %d;" % (subject, movie_index)
                self.conn.execute(sql1)
                self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
