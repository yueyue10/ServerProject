from django.db import models
from datetime import date
from django.urls import reverse


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


# 书籍数据
class Book(models.Model):
    bookName = models.CharField(max_length=15)
    image = models.URLField()
    author = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    desc = models.TextField(null=True)
    chapters = models.TextField(null=True)

    def __str__(self):
        return self.bookName


# 书籍章节数据
class BookChapter(models.Model):
    bookName = models.CharField(max_length=15)
    title = models.TextField(null=True)
    paragraphs = models.TextField(null=True)

    def __str__(self):
        return self.bookName


# 合称数据
class MergeInfo(models.Model):
    title = models.CharField(max_length=15)
    desc = models.TextField(null=True)
    data = models.TextField(null=True)
    flag = models.CharField(max_length=10, default='flag')

    def __str__(self):
        return self.title


# 热映电影
class HotMovie(models.Model):
    date = models.DateField(auto_now=True)
    dateId = models.CharField(max_length=15)
    movies = models.TextField(null=True)

    def __str__(self):
        return self.dateId


# 电影数据
class Movie(models.Model):
    flag = models.CharField(max_length=10)
    movie_index = models.IntegerField(null=True)
    title = models.CharField(max_length=15)
    image = models.TextField(null=True)
    subject = models.TextField(null=True)
    director = models.TextField(null=True)
    actor = models.TextField(null=True)
    area = models.TextField(null=True)
    mtime = models.TextField(null=True)
    mtype = models.TextField(null=True)
    score = models.TextField(null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.title


# 电影详情
class MovieDetail(models.Model):
    subjectId = models.CharField(max_length=15)
    title = models.TextField()
    image = models.TextField()
    score = models.CharField(max_length=5)
    pubdateTime = models.CharField(max_length=20)
    movieType = models.CharField(max_length=20)
    duration = models.CharField(max_length=15)
    director = models.CharField(max_length=20)
    area = models.CharField(max_length=15)
    intro = models.TextField()
    comments = models.TextField()
    actors = models.TextField()
    tags = models.TextField()
    photos = models.TextField()


class Picture(models.Model):
    title = models.CharField("标题", max_length=100, blank=True, default='')
    image = models.ImageField("图片", upload_to="images", blank=True)
    date = models.DateField(default=date.today)


def __str__(self):
    return self.title
