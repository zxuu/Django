from django.db import models

# Create your models here.
class User(models.Model):
    # 默认id
    id= models.CharField(max_length=36,primary_key='True')
    # 名字，字符串字段，最大长度36位，默认字符KirisameMarisa，允许为空
    name = models.CharField(max_length=36, null='False')
    # 年龄，整型字段，最大长度5，不允许位空
    age = models.CharField(max_length=5, null="False")

    class Meta:
        db_table = "User"

class Img(models.Model):
    name = models.CharField(max_length=200,default="data")
    img_url = models.ImageField(upload_to='igg') # upload_to指定图片上传的途径，如果不存在则自动创建
    # name = models.CharField(max_length=255,primary_key=True)

class Image(models.Model):
    url = models.CharField(max_length=252)
    class Meta:
        db_table = "Image"

class Viedeo(models.Model):
    url = models.CharField(max_length=252)
    class Meta:
        db_table = 'Video'