import codecs
import json
import random
import sqlite3
import time
import datetime

import requests
from lxml import etree

from miniprogram.models import HotMovie
from miniprogram.utils import ComHeaders
from miniprogram.utils.StringUtils import format_str_info

HOT_Url = 'https://movie.douban.com/cinema/nowplaying/beijing/'


# 电影实体类
class MovieBean(object):
    def __init__(self, subject, title, image, score, director, actor, duration, area):
        self.subject = format_str_info(subject)
        self.title = format_str_info(title)
        self.image = format_str_info(image)
        self.score = format_str_info(score)
        self.director = format_str_info(director)
        self.actor = format_str_info(actor)
        self.duration = format_str_info(duration)
        self.area = format_str_info(area)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class HotMovieSpider(object):
    url = HOT_Url

    def __init__(self):
        self.today = datetime.date.today()
        self.conn = sqlite3.connect('../../db.sqlite3')
        print('open database successfully')

    def start(self):
        movie_hot_in_db = self.get_db_movie_hot()
        if movie_hot_in_db:
            self.conn.close()
            movieHot = movie_hot_in_db[0]
            movieList = json.loads(movieHot.movies)
        else:
            movieList = self.get_info_from_movie(self.url)
            self.save_db_movie(movieList)
            self.conn.close()
        movieList_json = json.dumps(movieList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        # print(movieList)
        # self.save_json_in_json("电影热映", movieList_json)
        return movieList_json

    def get_db_movie_hot(self):
        print('get_db_movie_hot')
        queryset = HotMovie.objects.filter(dateId=self.today)
        movie_result = list(queryset)
        print("movie_result-----------", movie_result)
        return movie_result

    def save_db_movie(self, movieList):
        movieListStr = self.get_obj_str(movieList)
        # print("movieListStr", movieListStr)
        movie_detail = HotMovie(dateId=self.today, movies=movieListStr)
        movie_detail.save()
        print('save_db_movie-保存成功')

    @staticmethod
    def get_obj_str(obj):
        obj_json = json.dumps(obj, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        # print(obj_json)
        return obj_json

    # 获取电影数据
    def get_info_from_movie(self, href):
        html_detail = self.get_html_text(href)
        com_html = etree.HTML(html_detail)
        movieLis = com_html.xpath('//*[@id="nowplaying"]/div[@class="mod-bd"]/ul/li')
        movieList = []
        for index, movieItem in enumerate(movieLis):
            if index == 6:
                break
            subject = movieItem.xpath('./@data-subject')[0]
            title = movieItem.xpath('./@data-title')[0]
            director = movieItem.xpath('./@data-director')[0]
            actor = movieItem.xpath('./@data-actors')[0]
            area = movieItem.xpath('./@data-region')[0]
            duration = movieItem.xpath('./@data-duration')[0]
            score = movieItem.xpath('./@data-score')[0]
            image = movieItem.xpath('./ul/li[@class="poster"]/a/img/@src')[0]
            movieBean = MovieBean(subject, title, image, score, director, actor, duration, area)
            movieList.append(movieBean)
        return movieList

    # 获取html页码内容
    @staticmethod
    def get_html_text(url, headers=None):
        time.sleep(random.uniform(0.5, 1.5))
        response = requests.get(url, headers=ComHeaders.pc_headers, timeout=(5, 60))
        html_text = ''
        if response.status_code == 200:
            html_text = response.text
        return html_text

    # 保存json数据到json文件中
    @staticmethod
    def save_json_in_json(name, jsonstr):
        with codecs.open('{}.json'.format(name), 'w', 'utf-8') as f:
            f.write(jsonstr)


if __name__ == '__main__':
    spider = HotMovieSpider()
    spider.start()
