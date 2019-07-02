from django.db import models

# Create your models here.
class User(models.Model):


    # 默认id
    name = models.CharField(max_length=50,primary_key='True')
    # 名字，字符串字段，最大长度36位，默认字符KirisameMarisa，允许为空
    tel = models.CharField(max_length=30)
    # 年龄，整型字段，最大长度5，不允许位空
    gender = models.CharField(max_length=5)
    declaration = models.CharField(max_length=255)
    back_img_url = models.CharField(max_length=255)
    pass_word = models.CharField(max_length=255)

    class Meta:
        db_table = "User"

class Img(models.Model):
    name = models.CharField(max_length=200,default="data")
    img_url = models.ImageField(upload_to='images') # upload_to指定图片上传的途径，如果不存在则自动创建
    # name = models.CharField(max_length=255,primary_key=True)

class Image(models.Model):
    time_image = models.CharField(max_length=255, primary_key='True')
    url_image = models.CharField(max_length=255)
    user_name = models.CharField(max_length=50)
    target_video = models.CharField(max_length=255)
    class Meta:
        db_table = "Image"

class Video(models.Model):
    url_video = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    heart_num = models.CharField(max_length=30)
    id_video =  models.CharField(max_length=255,primary_key='True')
    class Meta:
        db_table = 'Video'

class Follow(models.Model):
    id = models.CharField(max_length=255,primary_key='True')
    user = models.CharField(max_length=255)
    user_target = models.CharField(max_length=255)
    class Meta:
        db_table = 'Follow'

class Comment(models.Model):
    id = models.CharField(max_length=100,primary_key='True')
    content = models.CharField(max_length=255)
    target_video = models.CharField(max_length=255)
    class Meta:
        db_table = 'Comment'