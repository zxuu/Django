from .models import User
from .models import Image
from rest_framework import serializers as mongo_serializers
from django.core import serializers

# 名字随意
class UserSerializer(mongo_serializers.ModelSerializer):
    class Meta:
        # 对应类名
        model = User
        # 各个字段，其中_id是默认id字段
        fields = ('id', 'name', 'age')

class ImgUrlSerializer(mongo_serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url')