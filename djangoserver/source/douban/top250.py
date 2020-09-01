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
                movie_index = int(movieObj['index'])
                print('line', movie_index, movieObj['title'])
                # 一、插入电影数据表数据
                sql1 = 'insert into miniprogram_movie(flag,movie_index,title,image,director,actor,area,mtime,mtype,score,comment) values("%s",%d,"%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    "电影TOP250", movie_index, movieObj['title'], movieObj['image'], movieObj['director'],
                    movieObj['actor'], movieObj['area'], movieObj['mtime'], movieObj['mtype'], movieObj['score'],
                    movieObj['comment'])
                self.conn.execute(sql1)
                self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
