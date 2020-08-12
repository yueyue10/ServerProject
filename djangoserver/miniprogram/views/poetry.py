from djangoserver import result

from miniprogram import models


# 获取年级列表数据
def grade_list(request, **kw):
    grade_types = models.GradeType.objects.all().values('grade_name', 'grade_image')
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
