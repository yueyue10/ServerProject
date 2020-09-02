import codecs
import json
import random
import time

import requests
from lxml import etree

from miniprogram.utils import ComHeaders
from miniprogram.utils.StringUtils import format_str_info, format_str_list, convert_list_to_str

simple_id = '26348103'
Detail_Url = 'https://movie.douban.com/subject/{}/'


# 电影实体类
class MovieBean(object):
    def __init__(self, image, title, score, pubdate_time, movie_type, duration, director,
                 area, intro, comments, actors, tags, photos):
        self.image = format_str_info(image)
        self.title = format_str_info(title)
        self.score = format_str_info(score)
        self.pubdateTime = format_str_info(pubdate_time)
        self.movieType = format_str_info(movie_type)
        self.duration = format_str_info(duration)
        self.director = format_str_info(director)
        self.area = format_str_info(area)
        self.intro = format_str_info(intro)
        self.comments = comments
        self.actors = actors
        self.photos = photos
        self.tags = tags

    def __str__(self):
        return "".join(str(item) for item in (self.title, self.image, self.score, self.pubdateTime, self.movieType,
                                              self.duration, self.director, self.area, self.intro, self.comments,
                                              self.actors, self.photos, self.tags))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    class ActorBean(object):

        def __init__(self, name, image):
            self.name = format_str_info(name)
            self.image = format_str_info(image)

        def __str__(self):
            return "".join(str(item) for item in (self.name, self.image))

    class CommentBean(object):

        def __init__(self, name, avatar, score, create_time, content):
            self.name = format_str_info(name)
            self.avatar = format_str_info(avatar)
            self.score = format_str_info(score)
            self.createTime = format_str_info(create_time)
            self.content = format_str_info(content)

        def __str__(self):
            return "".join(str(item) for item in (self.name, self.avatar, self.score, self.createTime, self.content))


class MovieDetailSpider(object):
    url = Detail_Url.format(simple_id)

    def __init__(self, movie_id=''):
        if movie_id: self.url = Detail_Url.format(movie_id)

    def start(self):
        movieBean = self.get_info_from_movie(self.url)
        movieBean_json = json.dumps(movieBean, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        # print(movieBean_json)
        return movieBean_json

    # 获取电影数据
    def get_info_from_movie(self, href):
        html_detail = self.get_html_text(href)
        com_html = etree.HTML(html_detail)
        article_html = com_html.xpath('//*[@class="article"]')[0]
        movie_top = article_html.xpath('./div[@class="indent clearfix"]/div[@class="subjectwrap clearfix"]')[0]
        movie_top_left = movie_top.xpath('./div[@class="subject clearfix"]')[0]

        score = movie_top.xpath('./div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]/'
                                'div[@class="rating_self clearfix"]/strong/text()')[0]
        intro = article_html.xpath('./div[@class="related-info"]/div[@class="indent"]/span/text()')[0]
        image = movie_top_left.xpath('./div[@id="mainpic"]/a/img/@src')[0]
        title = com_html.xpath('//*[@id="content"]/h1/span/text()')
        title = convert_list_to_str(title)
        movieInfo = self.get_movie_info_dict(movie_top_left)
        actors = self.get_movie_actors(article_html)
        tags = self.get_movie_tags(com_html)
        all_photos = self.get_movie_photos(href)
        comments = self.get_movie_comment(article_html)
        movieBean = MovieBean(image, title, score, movieInfo['pubdate_time'], movieInfo['movie_type'],
                              movieInfo['duration'], movieInfo['director'], movieInfo['area'], intro, comments,
                              actors, tags, all_photos)
        return movieBean

    @staticmethod
    def get_movie_comment(article_html):
        comment_beans = []
        comment_list = article_html.xpath(
            './div[@id="comments-section"]/div[@class="mod-bd"]/div[@class="tab-bd"]/div[@id="hot-comments"]/div['
            '@class="comment-item"]')
        for comment in comment_list:
            comment_user = comment.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/a/text()')[0]
            comment_score = comment.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@class')[0]
            comment_time = comment.xpath('./div[@class="comment"]/h3/span[@class="comment-info"]/span['
                                         '@class="comment-time "]/text()')[0]
            comment_score = comment_score.replace('allstar', '').replace(' rating', '')
            comment_text = comment.xpath('./div[@class="comment"]/p/span/text()')[0]
            commentBean = MovieBean.CommentBean(comment_user, '', comment_score, comment_time, comment_text)
            comment_beans.append(commentBean)
            # print(comment_user, comment_score, comment_time, comment_text)
        # print(comment_list)
        return comment_beans

    def get_movie_photos(self, href):
        photo_url = href + "all_photos"
        html_detail = self.get_html_text(photo_url)
        com_html = etree.HTML(html_detail)
        photo_lis = com_html.xpath('//*[@class="article"]/div[1]/div[@class="bd"]/ul/li')
        # print(photo_lis)
        all_photos = []
        for photo_li in photo_lis:
            photo_url = photo_li.xpath('./a/img/@src')[0]
            # print(photo_li, photo_url)
            all_photos.append(photo_url)
        return all_photos

    @staticmethod
    def get_movie_tags(com_html):
        tags = com_html.xpath('//*[@class="aside"]/div[@class="tags"]/div[@class="tags-body"]/a/text()')
        tags = format_str_list(tags)
        return tags

    @staticmethod
    def get_movie_actors(article_html):
        actor_list = []
        actors = article_html.xpath('./div[@id="celebrities"]/ul/li')
        for actor in actors:
            image_style = actor.xpath('./a/div/@style')[0]
            image = image_style.replace('background-image: url(', '').replace(')', '')
            # print(image_style)
            actor_name = actor.xpath('./div/span[@class="name"]/a/text()')[0]
            actor_desc = actor.xpath('./div/span[@class="role"]/text()')[0]
            # print(actor_name, actor_desc)
            actor_str = "{}({})".format(actor_name, actor_desc)
            actorBean = MovieBean.ActorBean(actor_str, image)
            actor_list.append(actorBean)
        # print(actor_list)
        return actor_list

    def get_movie_info_dict(self, movie_top):
        movieDict = {'pubdate_time': '', 'movie_type': '', 'duration': '', 'director': '', 'area': ''}
        movie_infos = self.get_movie_info(movie_top)
        for info in movie_infos:
            if info.find("导演:") >= 0:
                movieDict['director'] = info.replace("导演:", "")
            if info.find("类型:") >= 0:
                movieDict['movie_type'] = info.replace("类型:", "")
            if info.find("片长:") >= 0:
                movieDict['duration'] = info.replace("片长:", "")
            if info.find("上映日期:") >= 0:
                movieDict['pubdate_time'] = info.replace("上映日期:", "")
            if info.find("制片国家/地区:") >= 0:
                movieDict['area'] = info.replace("制片国家/地区:", "")
        return movieDict

    def get_movie_info(self, movie_top):
        # 获取div[@id="info"]下的所有子标签
        movie_infos = movie_top.xpath('./div[@id="info"]/child::*')
        movie_txts = movie_top.xpath('./div[@id="info"]/text()')
        movie_brs = movie_top.xpath('./div[@id="info"]/br')
        movie_txts = self.format_str_lists(movie_txts)  # 存储div下的所有文本标签，过滤掉特殊字符及/字符
        # movie_maps存放电影Map信息集合
        index = 0
        movie_maps = []
        for movie_br in movie_brs:
            movie_spans = []
            for info_index, movie_info in enumerate(movie_infos):
                if info_index < index:  # 当前标识小于总标识则跳过
                    continue
                else:  # 否则继续执行
                    index = index + 1
                    if movie_br != movie_info:  # 如果当前标签不是br标签，则添加到span数据集合movie_spans中
                        movie_spans.append(movie_info)
                    else:  # 否则将movie_spans集合数据添加到电影map集合movie_maps中
                        movie_maps.append(movie_spans)
                        break

        # print(len(movie_maps))
        # 遍历电影Map信息集合
        movie_strs = []
        txt_index = 0
        for movie_map_index, movie_map in enumerate(movie_maps):
            movie_str = ''
            if len(movie_map) == 1:  # 如果是单个span标签
                span_class = movie_map[0].xpath('./@class')
                if span_class and span_class[0] == 'pl':  # 如果标签的class是pl：数据在span标签及span后面
                    movie_str = movie_map[0].text + movie_txts[txt_index]
                    txt_index = txt_index + 1
                else:  # 否则：数据在span标签的子标签里面
                    movie_key = movie_map[0].xpath('./span[@class="pl"]/text()')
                    if movie_key: movie_key = self.convert_list_to_str(movie_key)
                    movie_value = movie_map[0].xpath('./span[@class="attrs"]/a/text()')
                    if movie_value: movie_value = self.convert_list_to_str(movie_value)
                    # print(movie_key, movie_value)
                    if movie_key and movie_value: movie_str = movie_key + ":" + movie_value
            else:  # 数据在多个span标签里面
                for map_index, movie_info_map in enumerate(movie_map):
                    if map_index == 0 or map_index == 1:
                        movie_str = movie_str + movie_info_map.text
                    else:
                        movie_str = movie_str + "/" + movie_info_map.text
            if movie_str:
                movie_strs.append(movie_str)
        # print(movie_strs)
        return movie_strs

    @staticmethod
    def format_str_lists(str_list):
        str_list = format_str_list(str_list)
        strs = []
        for str in str_list:
            if str != '/':
                strs.append(str)
        return strs

    @staticmethod
    def convert_list_to_str(str_list):
        result = ""
        for index, strr in enumerate(str_list):
            if index == 0:
                result = result + strr
            else:
                result = result + "/" + strr
        return result

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
    spider = MovieDetailSpider()
    spider.start()
