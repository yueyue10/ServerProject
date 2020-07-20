from django.conf.urls import url
from django.urls import path

from miniprogram import views

urlpatterns = [
    path('index/', views.index),
    url(r'grade_types/', views.grade_types),
    url(r'poetry_rank/', views.poetry_rank),
    path(r'poetry_list/', views.poetry_list),  # 第一种方式：通过请求参数传值
    path(r'poetry/<int:poetry_flag>', views.poetry),  # 第二种方式：通过方法参数传值
]
