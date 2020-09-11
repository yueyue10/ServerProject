import codecs
import json
import random
import time

import requests
from lxml import etree

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

    def start(self):
        movieList = self.get_info_from_movie(self.url)
        movieList_json = json.dumps(movieList, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        # print(movieList)
        # self.save_json_in_json("电影热映", movieList_json)
        # print(colorListBean_json)
        return movieList_json

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
