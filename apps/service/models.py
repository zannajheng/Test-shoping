from django.db import models

# Create your models here.
# 表情包
class Face(models.Model):
    name = models.CharField(max_length=255, verbose_name='名字')
    image = models.CharField(max_length=255, verbose_name='文件名')


    class Meta:
        db_table = 'face'
        verbose_name = '表情包'