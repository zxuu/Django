"""djangoDemo2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from service import views
from django.conf.urls import url
from djangoDemo2 import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

# 定义url，移动端通过这个url访问服务端
    url(r'^users/$', views.user_api),
    # username就是之前views中another_user_api方法中的参数
    url(r'^users/(?P<username>[A-Za-z0-9]+)/$', views.another_user_api),
    # 安卓端用api
    url(r'^android_user/$', views.android_user_api),
    # 上传图片
    url(r'^uploadImage/$', views.uploadImages),
    #上传视频相册
    url(r'^uploadVideo/$', views.uploadVideo),
    url(r'^uploadFile/$', views.upLoadFile),
    #注册
    url(r'^register/$',views.register),
    #登录
    url(r'^sign/$',views.sign),
    #评论
    url(r'^putComment/$',views.putComment),
    #关注
    url(r'^putFollow/$',views.putFollow),
    #点赞
    url(r'^putDianZan/$',views.putDianZan),

    #获取我的视频相册
    url(r'^getVideos/$', views.getVideos),
    #获取我的相册集
    url(r'^getImages/$', views.getImages),
    #获取视频相关的用户
    url(r'^getUser/$', views.getUser),
    #获取视频相册对应相册集
    url(r'^getVideoImages/$', views.getVideoImages),
    #获取我关注的人
    url(r'^getFollows/$', views.getFollows),
    #//获取视频对应的评论
    url(r'^getComments/$', views.getComments),

    url(r'^uploading/$', views.uploadImg),
    url(r'^showImg/$', views.showImg),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
