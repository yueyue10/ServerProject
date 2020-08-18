from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djangoserver import result
from miniprogram import models
# 获取诗词列表数据
from miniprogram.models import GradeType, Poetry, MarkType, MergeInfo, Book, BookChapter
from miniprogram.serializers import GradeTypeSerializer, ResultPagination, PoetrySerializer, MarkTypeSerializer, \
    MergeInfoSerializer, PoetryInfoSerializer, BookSerializer, BookChapterSerializer


@api_view(['GET'])
def poetry_list(request, format=None):
    """
    获取诗词列表数据
    limit: 每页数量
    offset: 页码数,从零开始
    poetryFlag: 诗词标识
    """
    poetry_flag = request.GET.get('poetryFlag')
    if not poetry_flag:
        return result.error('poetry_flag参数错误', {})
    poetry_list_data = Poetry.objects.filter(poetry_flag=poetry_flag)
    obj = ResultPagination()
    page_list = obj.paginate_queryset(poetry_list_data, request)
    ser = PoetrySerializer(instance=page_list, many=True)
    response = obj.get_paginated_response(ser.data)
    return response


@api_view(['GET'])
def grade_list(request, format=None):
    """
    获取年级列表数据
    """
    grade_types = GradeType.objects.all()
    serializer = GradeTypeSerializer(grade_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def grade_poetry(request, **kw):
    """
    获取年级分类诗词数据
    grade_name: 年级名称-一年级上册
    """
    grade_name = request.GET.get('grade_name')
    print('grade_name', grade_name)
    if not grade_name:
        return result.error('grade_name参数错误', {})
    grade_types = GradeType.objects.filter(grade_name=grade_name).values('poetry_flag')
    poetry_flag = grade_types[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = Poetry.objects.filter(poetry_flag=poetry_flag)
    obj = ResultPagination()
    page_list = obj.paginate_queryset(poetry_list_data, request)
    ser = PoetrySerializer(instance=page_list, many=True)
    response = obj.get_paginated_response(ser.data)
    return response


@api_view(['GET'])
def mark_list(request, **kw):
    """
    获取分类列表数据
    """
    mark_types = MarkType.objects.all()
    serializer = MarkTypeSerializer(mark_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def mark_poetry(request, **kw):
    """
    获取分类诗词数据
    mark_name: 分类名称-田园诗
    """
    mark_name = request.GET.get('mark_name')
    print('mark_name', mark_name)
    if not mark_name:
        return result.error('mark_name参数错误', {})
    mark_flag_data = MarkType.objects.filter(mark_name=mark_name).values('poetry_flag')
    poetry_flag = mark_flag_data[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = Poetry.objects.filter(poetry_flag=poetry_flag)
    obj = ResultPagination()
    page_list = obj.paginate_queryset(poetry_list_data, request)
    ser = PoetrySerializer(instance=page_list, many=True)
    response = obj.get_paginated_response(ser.data)
    return response


@api_view(['GET'])
def merge_info(request, **kw):
    """
    获取合称列表数据
    merge_flag: 合称标识-史书典籍
    """
    merge_flag = request.GET.get('merge_flag')
    print('merge_flag', merge_flag)
    if not merge_flag:
        return result.error('merge_flag参数错误', {})
    merge_data = MergeInfo.objects.filter(flag=merge_flag)
    serializer = MergeInfoSerializer(merge_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def rank_poetry(request, **kw):
    """
    获取排行榜列表数据
    """
    poetry_flag_data = models.PoetryFlag.objects.filter(poetry_type='诗词排行榜').values('poetry_type', 'poetry_flag')
    poetry_flag = poetry_flag_data[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = Poetry.objects.filter(poetry_flag=poetry_flag)
    obj = ResultPagination()
    page_list = obj.paginate_queryset(poetry_list_data, request)
    ser = PoetryInfoSerializer(instance=page_list, many=True)
    response = obj.get_paginated_response(ser.data)
    return response


@api_view(['GET'])
def book_info(request, **kw):
    """
    获取书籍数据
    bookName: 书籍名称-《三国演义》
    """
    book_name = request.GET.get('bookName')
    print('bookName', book_name)
    if not book_name:
        return result.error('bookName参数错误', {})
    book_data = Book.objects.filter(bookName=book_name)
    print('book_data', book_data)
    book_ser = BookSerializer(book_data, many=True)
    return Response(book_ser.data)


@api_view(['GET'])
def book_chapter(request, **kw):
    """
    获取书籍章节数据
    bookName: 书籍名称-《三国演义》
    chapter: 章节名称-第一回·宴桃园豪杰三结义斩黄巾英雄首立功
    """
    book_name = request.GET.get('bookName')
    chapter = request.GET.get('chapter')
    print('bookName', book_name, chapter)
    if not book_name:
        return result.error('bookName参数错误', {})
    if not chapter:
        return result.error('chapter参数错误', {})
    chapter_data = BookChapter.objects.filter(bookName=book_name, title=chapter)
    book_ser = BookChapterSerializer(chapter_data, many=True)
    return Response(book_ser.data)
