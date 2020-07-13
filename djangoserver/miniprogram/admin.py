from django.contrib import admin

# Register your models here.
from miniprogram import models

admin.site.register(models.Poetry)
admin.site.register(models.PoetryFlag)
admin.site.register(models.GradeType)
admin.site.register(models.MarkType)
