from .models import User
from .models import Image,Video
from rest_framework import serializers as mongo_serializers
from django.core import serializers

# 名字随意
class UserSerializer(mongo_serializers.ModelSerializer):
    class Meta:
        # 对应类名
        model = User
        # 各个字段，其中_id是默认id字段
        fields = ('name', 'tel', 'gender','declaration','back_img_url')

class ImgUrlSerializer(mongo_serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('time_image','url_image','user_name','target_video')

class VideoUrlSerializer(mongo_serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('url_video','user_name','heart_num','id_video')