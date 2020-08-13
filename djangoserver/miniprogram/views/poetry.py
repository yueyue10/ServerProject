from django.core.paginator import Paginator

from djangoserver import result

from miniprogram import models


# 获取诗词列表数据
def poetry_list(request, **kw):
    page_num = request.GET.get('pageNum')
    page_index = request.GET.get('pageIndex')
    poetry_flag = request.GET.get('poetryFlag')
    print('poetry_flag', poetry_flag, page_num, page_index)
    if not poetry_flag:
        return result.error('poetry_flag参数错误', {})
    poetry_list_data = models.Poetry.objects.filter(poetry_flag=poetry_flag).values('title', 'time', 'author',
                                                                                    'content', 'pic')
    if page_num and page_index:
        paginator = Paginator(poetry_list_data, page_num)
        page_num = paginator.num_pages
        page_list = paginator.page(page_index)
        poetry_obj = {
            'count': page_num,
            'current': page_index,
            'list': list(page_list)
        }
        return result.success(poetry_obj)
    else:
        return result.success(list(poetry_list_data))


# 获取年级列表数据
def grade_list(request, **kw):
    grade_types = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
    return result.success(list(grade_types))


# 获取年级分类诗词数据
def grade_poetry(request, **kw):
    grade_name = request.GET.get('grade_name')
    print('grade_name', grade_name)
    if not grade_name:
        grade_name = '一年级上册'
    poetry_flag_data = models.GradeType.objects.filter(grade_name=grade_name).values('poetry_flag')
    poetry_flag = poetry_flag_data[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = models.Poetry.objects.filter(poetry_flag=poetry_flag).values('title', 'time', 'author',
                                                                                    'content', 'pic')
    return result.success(list(poetry_list_data))


# 获取分类列表数据
def mark_list(request, **kw):
    mark_types = models.MarkType.objects.all().values('mark_name', 'mark_image', 'mark_time', 'mark_author',
                                                      'poetry_flag')
    return result.success(list(mark_types))


# 获取分类诗词数据
def mark_poetry(request, **kw):
    mark_name = request.GET.get('mark_name')
    print('mark_name', mark_name)
    if not mark_name:
        mark_name = '田园诗'
    mark_flag_data = models.MarkType.objects.filter(mark_name=mark_name).values('poetry_flag')
    poetry_flag = mark_flag_data[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = models.Poetry.objects.filter(poetry_flag=poetry_flag).values('title', 'time', 'author',
                                                                                    'content', 'pic')
    return result.success(list(poetry_list_data))


# 获取合称列表数据
def merge_info(request, **kw):
    merge_flag = request.GET.get('merge_flag')
    print('rank_flag', merge_flag)
    if not merge_flag:
        # merge_flag = '作者合称大全'
        merge_flag = '史书典籍'
    merge_data = models.MergeInfo.objects.filter(flag=merge_flag).values('title', 'desc', 'data', 'flag')
    return result.success(list(merge_data))


# 获取排行榜列表数据
def rank_poetry(request, **kw):
    poetry_flag_data = models.PoetryFlag.objects.filter(poetry_type='诗词排行榜').values('poetry_type', 'poetry_flag')
    poetry_flag = poetry_flag_data[0]['poetry_flag']
    print('poetry_flag', poetry_flag)
    poetry_list_data = models.Poetry.objects.filter(poetry_flag=poetry_flag).values('title', 'time', 'author',
                                                                                    'content', 'pic', 'mark_index')
    return result.success(list(poetry_list_data))


# 获取书籍数据
def book_info(request, **kw):
    book_name = request.GET.get('bookName')
    print('bookName', book_name)
    if not book_name:
        book_name = '《三国演义》'
    book_data = models.Book.objects.filter(bookName=book_name).values('bookName', 'image', 'author', 'year',
                                                                      'desc', 'chapters')
    book_obj = {}
    if len(book_data) > 0:
        book_obj = list(book_data)[0]
    return result.success(book_obj)


# 获取书籍章节数据
def book_chapter(request, **kw):
    chapter_obj = {}
    book_name = request.GET.get('bookName')
    chapter = request.GET.get('chapter')
    print('bookName', book_name, chapter)
    if not book_name:
        book_name = '《三国演义》'
    if not chapter:
        return result.error('chapter参数错误', chapter_obj)
    chapter_data = models.BookChapter.objects.filter(bookName=book_name, title=chapter).values('paragraphs', 'title',
                                                                                               'bookName')
    return result.success(list(chapter_data))
