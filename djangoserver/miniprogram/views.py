import json

from django.shortcuts import HttpResponse

# Create your views here.
from djangoserver import result
from miniprogram import models


def index(request):
    queryset = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
    ret = json.dumps(list(queryset), ensure_ascii=False)
    return HttpResponse(ret)


def grade_types(request):
    queryset = models.GradeType.objects.all().values('grade_name', 'grade_image', 'poetry_flag')
    print(queryset, '\n', type(queryset))
    return result.success(list(queryset))
