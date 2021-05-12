import json
import time

from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, render
from django.conf import settings
from djangoserver import result
from miniprogram import models
import os
from miniprogram.answer.main import Answer
from miniprogram.models import Picture


def index(request):
    queryset = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
    ret = json.dumps(list(queryset), ensure_ascii=False)
    return HttpResponse(ret)


def upload(request):
    print("upload==========", request)
    if request.method == 'POST':  # 获取对象
        obj = request.FILES.get('image_input')
        print("name============", obj.name)
        picture = Picture(title=obj.name, image=obj)
        picture.save()
        file_path = os.path.join(settings.MEDIA_ROOT, picture.image.url)
        print("file_path============", file_path)
        answer = Answer(file_path)
        ans_list, points_name, file_name = answer.start()
        ans_num = len(ans_list)
        return render(request, 'upload.html',
                      {"imgName": file_name, "ans_list": ans_list, "ans_num": ans_num, "points_name": points_name})
    return render(request, 'upload.html', {"imgName": '', "ans_list": ''})


def upload_img(request):
    local_path = 'https://zhaoyj.work/media/images/'
    if request.method == 'POST':  # 获取对象
        obj = request.FILES.get('image_input')
        print("upload_img-obj=================", obj)
        picture = Picture(title=obj.name, image=obj)
        picture.save()
        file_path = os.path.join(settings.MEDIA_ROOT, picture.image.url)
        print("file_path============", file_path)
        answer = Answer(file_path)
        ans_list, points_name, file_name = answer.start()
        ans_num = len(ans_list)
        img_path = os.path.join(local_path, file_name)
        points_path = os.path.join(local_path, points_name)
        data = {"answers": ans_list, "ans_num": ans_num, "img_path": img_path, "points_path": points_path}
        return result.success(data)
        file = request.FILES['image_input']
        return HttpResponse(file, content_type="image/jpeg")


def grade_types(request):
    queryset = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
    # print(queryset)
    print(type(queryset))
    # print(list(queryset))
    return result.success(list(queryset))


# 第一种方式：获取方法参数里面的poetry_flag
def poetry(request, poetry_flag):
    queryset = models.Poetry.objects.filter(poetry_flag=poetry_flag).order_by('-mark_index').values('title', 'time',
                                                                                                    'author', 'content',
                                                                                                    'mark_index',
                                                                                                    'poetry_flag',
                                                                                                    'pic')
    # print(queryset)
    print(type(queryset))
    # print(list(queryset))
    return result.success(list(queryset))


# 第二种方式：获取请求参数里面的poetry_flag
def poetry_list(request, **kw):
    print('----------------------------', type(kw), kw)
    if kw:
        page_num = kw['page_num']
        page_index = kw['page_index']
        poetry_flag = kw['poetry_flag']
    else:
        page_num = request.GET.get('pageNum')
        page_index = request.GET.get('pageIndex')
        poetry_flag = request.GET.get('poetry_flag')
    queryset = models.Poetry.objects.filter(poetry_flag=poetry_flag).order_by('mark_index').values('title', 'time',
                                                                                                   'author', 'content',
                                                                                                   'mark_index',
                                                                                                   'poetry_flag',
                                                                                                   'pic')
    paginator = Paginator(queryset, page_num)
    page_num = paginator.num_pages
    page_list = paginator.page(page_index)
    # print(queryset)
    print(type(queryset))
    # print(list(queryset))
    poetry_obj = {
        'count': page_num,
        'current': page_index,
        'list': list(page_list)
    }
    return result.success(poetry_obj)


def poetry_rank(request):
    page_num = request.GET.get('pageNum')
    page_index = request.GET.get('pageIndex')
    rankFlag = models.PoetryFlag.objects.get(poetry_type='诗词排行榜')
    print(rankFlag)
    print(rankFlag.poetry_flag)
    return poetry_list(request, page_num=page_num, page_index=page_index, poetry_flag=rankFlag.poetry_flag)
