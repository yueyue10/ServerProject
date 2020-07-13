from django.db import models


# 诗词数据
class Poetry(models.Model):
    mark_index = models.IntegerField(null=True)
    title = models.CharField(max_length=15)
    time = models.CharField(max_length=5)
    author = models.CharField(max_length=10)
    content = models.TextField(null=True)
    pic = models.URLField(null=True)
    poetry_flag = models.IntegerField(db_index=True)

    def __str__(self):
        return self.title + self.author


# 诗词标识
class PoetryFlag(models.Model):
    poetry_type = models.CharField(max_length=8)
    poetry_flag = models.AutoField(primary_key=True)

    def __str__(self):
        return self.poetry_type


# 年级数据
class GradeType(models.Model):
    grade_name = models.CharField(max_length=15, )
    grade_image = models.URLField()
    poetry_flag = models.IntegerField(db_index=True)

    def __str__(self):
        return self.grade_name


# 分类数据
class MarkType(models.Model):
    mark_name = models.CharField(max_length=15)
    mark_image = models.URLField()
    mark_time = models.TextField(null=True)
    mark_author = models.TextField(null=True)
    poetry_flag = models.IntegerField(db_index=True)

    def __str__(self):
        return self.mark_name
