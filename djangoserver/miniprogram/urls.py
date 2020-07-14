from django.urls import path, include

from miniprogram import views

urlpatterns = [
    path('index/', views.index),
    path('gradeTypes/', views.grade_types)
]
