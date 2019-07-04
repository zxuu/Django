import random
import simplejson as simplejson
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Img,Image,Video,Follow,Comment
from .serializers import UserSerializer, ImgUrlSerializer,VideoUrlSerializer
from djangoDemo2 import settings
from datetime import datetime
import os
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect



# Create your views here.
# 规定该方法只能通过post、get和delete请求
@api_view(['POST', 'GET', 'DELETE'])
# request就是你的请求
def user_api(request):
    # 如果请求是get
    if request.method == 'GET':

        # 获取user表全部的用户
        users = User.objects.all()

        # 将获取结果序列化，当many=True的时候才允许返回多条数据，不然报错
        serializer = UserSerializer(users, many=True)

        # serializer.data是一个字典，status是状态码，2XX是成功返回
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 如果请求是post
    elif request.method == 'POST':

        # request.data也是一个字典，有兴趣可以 print(request.data)
        serializer = UserSerializer(data=request.data)

        # 如果数据符合规定，字符长度之类的
        if serializer.is_valid():
            # 保存
            serializer.save()

            # 同上
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 如果不符合规定
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 如果是delete请求
    elif request.method == 'DELETE':

        # 删除全部用户
        User.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 同上
@api_view(['GET', 'PUT', 'DELETE'])
# name是参数，这不是我常用的方法，仅仅是和大家说有这样的用法
def another_user_api(request, username):
    # 同上
    if request.method == 'GET':

        # 获取单个用户，其中name是字段名，username是参数
        # user = User.objects.get(name=username)

        # 由于我在models中没写不允许字段重复，所有get方法当有字段重复时会报错
        # filter就是根据条件查找，first很容易理解，就是第一条数据
        user = User.objects.filter(name=username).first()

        # 将结果序列化，不需要many=True
        serializer = UserSerializer(user)

        # 同上
        return Response(serializer.data, status=status.HTTP_200_OK)

    # put一般是修改
    elif request.method == 'PUT':

        # 同上
        user = User.objects.filter(name=username).first()

        # 同上，request.data是传入的要修改的新数据
        # 先把要修改的那条数据从数据库中获取，然后修改数据，保存
        serializer = UserSerializer(user, data=request.data)

        # 同样要检查数据合法性
        if serializer.is_valid():
            # 合法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            # 不合法
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        # 同上
        user = User.objects.filter(name=username).first()

        # 删除
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def android_user_api(request):
    if request.method == 'POST':
        _data = dict(request.data)
        print(_data)
        # 之前说过request.data是一个字典，可以利用这个
        if _data['method'][0] == '_GET':
            user = User.objects.get(name=_data['name'][0], age=_data['age'][0])
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif _data['method'][0] == '_POST':
            # request.data 中多余的数据不会保存到数据库中
            serializer = UserSerializer(data=request.data)
            print('data-------------->',request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif _data['method'][0] == '_PUT':
            user = User.objects.get(name=_data['name'][0])
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif _data['method'][0] == '_DELETE':
            User.objects.get(name=_data['name'][0]).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

#-------------上传图片----------------------------
def uploadImages(request):
    if True:
        sourcefiles = request.FILES['file']

        user_name = request.POST.get('myName')
        file_name = sourcefiles.name
        print(user_name)
        Image.objects.create(url_image="http://192.168.0.12:8000/media/images/"+file_name,user_name=user_name,time_image="2019.6.28")
        print('sourcefiles.content_type----------------->',sourcefiles.content_type)
        if sourcefiles.content_type == 'application/octet-stream' or sourcefiles.content_type == 'image/jpeg' or sourcefiles.content_type == 'application/x-jpg' or sourcefiles.content_type == 'image/png' or sourcefiles.content_type == 'application/x-png' or sourcefiles.content_type == 'text/plain':
            file_path = save_uploaded_file(sourcefiles, "images")
            data = {'file_path':file_path}
    else:
        data = {'error':'没有选择上传文件'}
    a = simplejson.dumps(data)
    return HttpResponse(a, 'application/javascript')

def save_uploaded_file(sourcefiles, fileType):
    # now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    filename = sourcefiles.name
    filePath = settings.MEDIA_ROOT + "/"+fileType+"/" + filename
    destination = open(filePath, 'wb+')
    try:
        for chunk in sourcefiles.chunks():
            destination.write(chunk)
    except Exception as e:
        print ("save_uploaded_file----%s : %s" % (Exception, e))
    finally:
        destination.close()
    data = {'file_path': "ok"}
    # a = simplejson.dumps(data)
    # return filePat
#------------上传视频-------------
def uploadVideo(request):
    print(request)
    if True:
        sourcefiles = request.FILES['files']
        file_name = sourcefiles.name
        user_name = request.POST.get('myName')
        now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        Video.objects.create(url_video="http://10.0.116.20:8080/"+file_name,user_name=user_name,heart_num="5",id_video=now)
        # print('sourcefiles.content_type----------------->',sourcefiles.content_type)
        if sourcefiles.content_type == 'application/octet-stream' or sourcefiles.content_type == 'image/jpeg' or sourcefiles.content_type == 'application/x-jpg' or sourcefiles.content_type == 'image/png' or sourcefiles.content_type == 'application/x-png' or sourcefiles.content_type == 'text/plain':
            file_path = save_uploaded_file(sourcefiles, "videos")
            data = {'result':"ok"}
    else:
        data = {'error':'没有选择上传文件'}
    a = simplejson.dumps(data)
    return HttpResponse(a, 'application/javascript')
#------------获取我的视频相册---------
def getVideos(request):
    userName = request.POST.get("myName")
    u = User.objects.filter(name=userName).first()
    userAll = User.objects.all()
    # rr = {'name': me.name, 'tel': me.tel, 'gender': me.gender, 'declaration': me.declaration, 'back_img_url': me.back_img_url}
    # xu = {}
    # xu['name'] = str(me.name)
    # xu['tel'] = str(me.name)
    # xu['gender'] = str(me.name)
    # xu['declaration'] = str(me.name)
    # xu['back_img_url'] = str(me.name)
    videos = Video.objects.all()
    # videosList = []
    # for video in videos:
    #     videosList.append(video.url_video)
    #     print(video.url_video)
    # print(videosList)
    # data = {'result': videosList}
    # a = json.dumps(data)
    # print(a)

    # result = {}
    # L = []
    # for v in videos:
    #     v.__dict__.pop("_state")
    #     L.append(v.__dict__)
    # result ['videos'] = L

    data = []
    for video in videos:
        d = {}
        d['url_video'] = video.url_video
        d['user_name'] = video.user_name
        d['heart_num'] = video.heart_num
        d['id_video'] = video.id_video
        data.append(d)


    userList = []
    for user in userAll:
        t = {}
        t['name'] = user.name
        t['tel'] = user.tel
        t['gender'] = user.gender
        t['declaration'] = user.declaration
        t['back_img_url'] = user.back_img_url
        userList.append(t)

    dd = {}
    dd['name'] = u.name
    dd['tel'] = u.tel
    dd['gender'] = u.gender
    dd['declaration'] = u.declaration
    dd['back_img_url'] = u.back_img_url

    # a = User(me.name,me.tel,me.gender,me.declaration,me.back_img_url)
    # mee = json.dumps(a.__dict__)
    result = {'result':data,'me':dd,'users':userList}
    print(result)
    a = simplejson.dumps(result)

    return HttpResponse(a, 'application/javascript')

def getUser(request):
    userName = request.POST.get("myName")
    u = User.objects.filter(name=userName).first()
    dd = {}
    dd['name'] = u.name
    dd['tel'] = u.tel
    dd['gender'] = u.gender
    dd['declaration'] = u.declaration
    dd['back_img_url'] = u.back_img_url
    result = {'me': dd}
    a = simplejson.dumps(result)

    return HttpResponse(a, 'application/javascript')


#------------获取我的相册集---------
def getImages(request):
    userName = request.POST.get("myName")
    images = Image.objects.filter(user_name=userName)
    # imagesList = []
    # imageTimeList = []
    # for image in images:
    #     imagesList.append(image.url_image)
    #     imageTimeList.append(image.time_image)
    # print(imagesList,imageTimeList)
    # data = {'img_url_list': imagesList,'img_time_list':imageTimeList}
    data = []
    for img in images:
        d = {}
        d['time_image'] = img.time_image
        d['url_image'] = img.url_image
        d['user_name'] = img.user_name
        d['target_video'] = img.target_video
        data.append(d)
    result = {'myImages':data}
    print(result)
    a = simplejson.dumps(result)
    return HttpResponse(a, 'application/javascript')

def getVideoImages(request):
    videoId = request.POST.get("videoId")
    images = Image.objects.filter(target_video=videoId)
    data = []
    for img in images:
        d = {}
        d['time_image'] = img.time_image
        d['url_image'] = img.url_image
        d['user_name'] = img.user_name
        d['target_video'] = img.target_video
        data.append(d)
    result = {'videoImages': data}
    print(result)
    a = simplejson.dumps(result)

    return HttpResponse(a, 'application/javascript')

def getFollows(request):
    userName = request.POST.get("myName")
    us = Follow.objects.filter(user=userName)
    name = []
    for i in us:
        name.append(i.user_target)
    print(name)
    data = []
    uy = User.objects.all()
    for u in uy:
        # print(i.name)
        if u.name in name:
            dd = {}
            dd['name'] = u.name
            dd['tel'] = u.tel
            dd['gender'] = u.gender
            dd['declaration'] = u.declaration
            dd['back_img_url'] = u.back_img_url
            data.append(dd)
    result = {'meFollows': data}
    a = simplejson.dumps(result)
    return HttpResponse(a, 'application/javascript')
def test(request):
    # userName = request.POST.get("myName")
    us = Follow.objects.filter(user="zxu")
    name = []
    for i in us:
        name.append(i.user_target)
    print(name)
    data = []
    uy = User.objects.all()
    for u in  uy:
        # print(i.name)
        dd = {}
        dd['name'] = u.name
        dd['tel'] = u.tel
        dd['gender'] = u.gender
        dd['declaration'] = u.declaration
        dd['back_img_url'] = u.back_img_url
        data.append(dd)
    result = {'me': data}
    a = simplejson.dumps(result)
    return HttpResponse(a, 'application/javascript')

def getComments(request):
    currVideoId = request.POST.get('currentVideo')
    comments = Comment.objects.filter(target_video=currVideoId)
    data = []
    for comment in comments:
        d = {}
        d['id'] = comment.id
        d['content'] = comment.content
        d['target_video'] = comment.target_video
        data.append(d)
    a = {'result':data}
    aa = simplejson.dumps(a)
    print(aa)
    return HttpResponse(aa, 'application/javascript')

#------上传文件--------
def upLoadFile(request):
    print(request)
    now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    sourcefiles = request.FILES.getlist('files')
    user_name = request.POST.get('myName')
    for source in sourcefiles:
        (filename, extension) = os.path.splitext(source.name)
        file_name = source.name
        if extension == '.mp4':
            Video.objects.create(url_video="http://10.0.116.20:8080/" + file_name, user_name=user_name,heart_num="0"
                                 ,id_video=now+"video")
            fn = save_uploaded_file(source, "videos")
            # return HttpResponse(fn, 'application/javascript')
        else:
            a = random.randint(0, 100)
            Image.objects.create(time_image=now+str(a),url_image="http://10.0.116.20:8000/media/images/" + file_name, user_name=user_name,
                                 target_video=now+"video")
            fn = save_uploaded_file(source, "images")
            # return HttpResponse(fn, 'application/javascript')
    return HttpResponse("result", 'application/javascript')

def register(request):
    sourcefiles = request.FILES['headPortrait']
    userName = request.POST.get('user_Name')
    userTel = request.POST.get('user_Tel')
    userPassWord = request.POST.get('user_PassW')
    userGender = request.POST.get('user_Gender')
    userDeclaration = request.POST.get('user_Dec')
    category = request.POST.get('category')
    if category == "0":
        if sourcefiles.content_type == 'application/octet-stream' or sourcefiles.content_type == 'image/jpeg' or sourcefiles.content_type == 'application/x-jpg' or sourcefiles.content_type == 'image/png' or sourcefiles.content_type == 'application/x-png' or sourcefiles.content_type == 'text/plain':
            save_uploaded_file(sourcefiles, "images")
            User.objects.create(name=userName, tel=userTel, gender=userGender
                                , declaration=userDeclaration, back_img_url=settings.imagesPath + sourcefiles.name
                                , pass_word=userPassWord)
            data = {'result': "ok"}
    else:
        data = {'result': "fail"}
    a = simplejson.dumps(data)
    return HttpResponse(a, 'application/javascript')

def sign(request):
    userName = request.POST.get('user_Name')
    userPassWord = request.POST.get('user_PassW')
    realUsere = User.objects.get(name=userName)
    if realUsere.pass_word == userPassWord:
        data = {'result': "ok"}
    else:
        data = {'result': "fail"}
    a = simplejson.dumps(data)
    print(a)
    return HttpResponse(a, 'application/javascript')

def putComment(request):
    now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    targetVideo = request.POST.get('currentVideo')
    content = request.POST.get('content')
    Comment.objects.create(id=now,content=content,target_video=targetVideo)
    data = {'result':"ok"}
    a = simplejson.dumps(data)
    print(a)
    return HttpResponse(a, 'application/javascript')

def putFollow(request):
    now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    me = request.POST.get('myName')
    tarName = request.POST.get('targetName')
    Follow.objects.create(id=now,user=me,user_target=tarName)
    data = {'result': "ok"}
    a = simplejson.dumps(data)
    print(a)
    return HttpResponse(a, 'application/javascript')

def putDianZan(request):
    tarVideo = request.POST.get('targetVideo')
    label = request.POST.get('label')
    video = Video.objects.get(id_video=tarVideo)
    if label == "1":
        video.heart_num = video.heart_num + 1
        video.save()
        data = {'result': "谢谢喜欢"}
    else:
        video.heart_num = video.heart_num - 1
        video.save()
        data = {'result': "不喜欢"}
    a = simplejson.dumps(data)
    return HttpResponse(a, 'application/javascript')


def uploadImg(request): # 图片上传函数
    if request.method == 'POST':
        img = Img(img_url=request.FILES.get('img'))
        print('-------------',img)
        img.save()
    return render(request, 'imagUpload.html')

def showImg(request):
    imgs = Img.objects.all() # 从数据库中取出所有的图片路径
    context = {
        'imgs' : imgs
    }
    return render(request, 'showImg.html', context)



