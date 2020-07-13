from django.db import models


# Create your models here.

class Poetry(models.Model):
    type = models.TextField(max_length=10, default='类型')
    title = models.CharField(max_length=10, default='名称')
    image = models.URLField()
    poetrys = models.TextField(null=True)

    def __str__(self):
        return self.type + self.title
