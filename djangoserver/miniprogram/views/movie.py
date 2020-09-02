import json

from rest_framework.decorators import api_view

# 获取诗词列表数据
from djangoserver import result
from miniprogram.models import Movie
from miniprogram.serializers import ResultPagination, MovieSerializer
from miniprogram.spider.spiderDetail import MovieDetailSpider
from miniprogram.spider.spiderHot import HotMovieSpider


@api_view(['GET'])
def top250(request, format=None):
    """
    获取电影TOP250数据
    limit: 每页数量
    offset: 页码数,从零开始
    """
    movie_list_data = Movie.objects.all()
    obj = ResultPagination()
    page_list = obj.paginate_queryset(movie_list_data, request)
    ser = MovieSerializer(instance=page_list, many=True)
    response = obj.get_paginated_response(ser.data)
    return response


def movie_hot(request, format=None):
    """
    获取热映电影数据
    limit: 每页数量
    offset: 页码数,从零开始
    """
    spider = HotMovieSpider()
    movieList = spider.start()
    movieListJson = json.loads(movieList)
    return result.success(movieListJson)


def movie_detail(request, format=None):
    """
    获取电影详情数据
    """
    movie_id = request.GET.get('movieId')
    if not movie_id:
        movie_id = '26348103'
    spider = MovieDetailSpider(movie_id)
    movieDetail = spider.start()
    movieDetailJson = json.loads(movieDetail)
    return result.success(movieDetailJson)
