from django.conf.urls import url
from django.urls import path

from miniprogram.views import poetry, index

urlpatterns = [
    path('index/', index.index),
    url(r'grade_types/', index.grade_types),
    url(r'poetry_rank/', index.poetry_rank),
    path(r'poetry_list/', index.poetry_list),  # 第一种方式：通过请求参数传值
    path(r'poetry/<int:poetry_flag>', index.poetry),  # 第二种方式：通过方法参数传值
    # 诗词数据接口
    path(r'grade/list', poetry.grade_list),
    path(r'grade/poetry', poetry.grade_poetry),
]
