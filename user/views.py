import os
import imghdr
import string
import secrets
import time
import filetype
from gmssl import sm2
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from index.models import *
from user.models import *
from .form import MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def loginView(request):
    user = MyUserCreationForm()
    if request.method == 'POST':
        if request.POST.get('loginUser', ''):
            u = request.POST.get('loginUser', '')
            p = request.POST.get('password', '')
            if MyUser.objects.filter(Q(username=u)):
                u1 = MyUser.objects.filter(Q(username=u)).first()
                if check_password(p, u1.password):
                    login(request, u1)
                    return redirect(reverse('home', kwargs={'page': 1}))
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        else:
            u = MyUserCreationForm(request.POST)
            if u.is_valid():
                u.save()
                if request.user.username:
                    uname = request.user.username
                    this_user_id = MyUser.objects.get(username=uname).id
                    user = MyUser.objects.get(id=this_user_id)
                    group = Group.objects.get(id=3)
                    user.groups.add(group)
                else:
                    print('用户组添加失败')
                tips = '注册成功'
            else:
                if u.errors.get('username', ''):
                    tips = u.errors.get('username', '注册失败')
                else:
                    tips = u.errors.get('password2','') + u.errors.get('email', '')
    return render(request, 'user.html', locals())


# 用户中心
# 设置用户登录限制
@login_required(login_url='/')
def homeView(request, page):
    # 热搜公文
    searchs = Dynamic.objects.select_related('document').order_by('-search').all()[:4]
    # 分页功能
    documents = request.session.get('play_list', [])
    paginator = Paginator(documents, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())


# 退出登录
def logoutView(request):
    logout(request)
    return redirect('/')


def uploadView(request):
    # 请求方法为POST时，执行文件上传
    if request.method == 'POST':
        # 获取上传的文件，如果没有文件，就默认为None
        myFile = request.FILES.get("myfile", None)
        summary = request.FILES.get("summary", None)
        image = request.FILES.get("image", None)
        if not myFile:
            return HttpResponse("上传的文件不可缺省")
        try:
            if str(myFile).endswith('.pdf'):
                pass
            else:
                return HttpResponse('文件不符合要求，请转为pdf文件')
        except:
            print('文件错误')
        try:
            if str(summary).endswith('.txt'):
                pass
            else:
                return HttpResponse('摘要不符合要求，请转为txt文件')
        except:
            print('摘要错误')
        try:
            if str(image).endswith('.jpg'):
                pass
            else:
                return HttpResponse('图片格式错误')
        except:
            print('图片错误')
        title = request.POST.get('title', '')
        office = request.POST.get('office', '')
        type_id = request.POST.get('type', '')

        if int(type_id) == 1:
            type='条例'
        elif int(type_id) == 2:
            type='请示'
        elif int(type_id) == 3:
            type='决定'
        elif int(type_id) == 4:
            type='命令'
        elif int(type_id) == 5:
            type='指示'
        elif int(type_id) == 6:
            type='批复'
        elif int(type_id) == 7:
            type='通知'
        elif int(type_id) == 8:
            type='通报'
        elif int(type_id) == 9:
            type='公告'
        elif int(type_id) == 10:
            type='通告'
        elif int(type_id) == 11:
            type='议案'
        elif int(type_id) == 12:
            type='报告'
        elif int(type_id) == 13:
            type='涵'
        elif int(type_id) == 14:
            type='会议纪要'
        else:
            type=''

        sec = int(request.POST.get('sec', ''))
        user = request.user.username
        now = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(16))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c in string.punctuation for c in password) <= 2
                    and sum(c.isdigit() for c in password) >= 3):
                break
        print(password)

        SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
        SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
        sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

        str1_bytes = bytes(password, encoding="utf8")
        str1_sm2en = sm2_crypt.encrypt(str1_bytes)
        print(str1_sm2en, len(str1_sm2en))

        article = Document(name=title, person=user, office=office, type=type, Classification=sec,
                           time=now, img=image, lyrics=summary, file=myFile, label_id=type_id, key=str1_sm2en)
        article.save()
        id = article.id
        dynamic = Dynamic(plays=0, search=0, download=0, document_id=id)
        dynamic.save()
        try:
            if imghdr.what(os.path.join("D://electronicDocument/media/documentImg/", str(image))) == None:
                print('img error')
            else:
                pass
        except:
            print('img test error')

        path_doc = os.path.join("D://electronicDocument/media/documentFile/", str(myFile))
        path_sum = os.path.join("D://electronicDocument/media/documentLyric/", str(summary))

        if file_test(path_doc):
            pass
        else:
            print('error document')
        if file_test(path_sum):
            pass
        else:
            print('error summary')

        file_reader = PdfFileReader("D:\\electronicDocument\\media\\documentFile\\"+str(myFile))
        file_writer = PdfFileWriter()
        for page in range(file_reader.getNumPages()):
            file_writer.addPage(file_reader.getPage(page))

        file_writer.encrypt(password)  # 设置密码
        with open("D:\\electronicDocument\\media\\documentFile\\"+str(myFile), 'wb') as out:
            file_writer.write(out)



        # 打开特定的文件进行二进制的写操作
        '''
        f = open(os.path.join("D://electronicDocument/media/documentFile/", myFile.name), 'wb+')
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        f = open(os.path.join("D://electronicDocument/media/documentLyric/", summary.name), 'wb+')
        # 分块写入文件
        for chunk in summary.chunks():
            f.write(chunk)
        f.close()
        f = open(os.path.join("D://electronicDocument/media/documentImg/", image.name), 'wb+')
        # 分块写入文件
        for chunk in image.chunks():
            f.write(chunk)
        f.close()
        '''
        return HttpResponse("上传成功")
    else:
        # 当请求方法为GET时，生成上传文件的页面
        return render(request, 'upload.html')


def file_test(path):
    kind = filetype.guess(path)
    if kind is None:
        print('Cannot guess file type!')
        return False
    elif kind.extension == 'exe':
        print(path + '是PE文件')
        return False
    else:
        return True