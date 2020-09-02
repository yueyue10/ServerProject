# miniprogram/serializers.py
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from miniprogram.models import Poetry, GradeType, MarkType, MergeInfo, Book, BookChapter, Movie


class ResultPagination(LimitOffsetPagination):
    # 默认每页显示的条数
    default_limit = 10
    # url 中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # url中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显示条数
    max_limit = None


class PoetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Poetry
        fields = ('title', 'time', 'author', 'content', 'pic')


class PoetryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poetry
        fields = "__all__"


class GradeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        fields = ('grade_name', 'grade_image', 'poetry_flag')


class MarkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkType
        fields = "__all__"


class MergeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MergeInfo
        fields = ('title', 'desc', 'data', 'flag')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('bookName', 'image', 'author', 'year', 'desc', 'chapters')


class BookChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = ('paragraphs', 'title', 'bookName')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'flag', 'movie_index', 'title', 'subject', 'image', 'director', 'actor', 'area', 'mtime', 'mtype', 'score',
            'comment')
