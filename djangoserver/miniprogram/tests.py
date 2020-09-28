import json
import sqlite3

import datetime

from django.test import TestCase


# Create your tests here.

def save_movie_in_db():
    conn = sqlite3.connect('../db.sqlite3')
    print('open database successfully')
    sql2 = 'insert into miniprogram_hotmovie( date,movies) values("%s","%s")' % (datetime.date.today(), "movieListStr")
    conn.execute(sql2)
    conn.commit()


def get_movie_in_db():
    conn = sqlite3.connect('../db.sqlite3')
    print('open database successfully')
    sql3 = "select * from miniprogram_hotmovie where date  = '%s'" % (datetime.date.today())
    sql3_result = conn.execute(sql3)
    movie_result = sql3_result.fetchall()
    conn.commit()
    print(movie_result)


if __name__ == '__main__':
    # save_movie_in_db()
    get_movie_in_db()
