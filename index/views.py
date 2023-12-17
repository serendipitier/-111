from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render
from user.models import MyUser
from .models import *
from gmssl import sm2


@login_required(login_url='/')
def indexView(request):
    if request.user.username:
        uname = request.user.username
        this_user = MyUser.objects.get(username=uname).is_secert
    else:
        this_user=0
    if not this_user:
        documentDynamic = Dynamic.objects.select_related('document').filter(document_id__Classification=this_user)
    else:
        documentDynamic = Dynamic.objects.select_related('document')
    # 热搜公文
    searchs = documentDynamic.order_by('-search').all()[:8]
    # 公文分类
    labels = Label.objects.all()
    # 热门公文
    popular = documentDynamic.order_by('-plays').all()[:10]
    # 最新公文
    recommend = Document.objects.order_by('-time').all()[:3]
    # 热门搜索、热门下载
    downloads = documentDynamic.order_by('-download').all()[:6]
    tabs = [searchs[:6], downloads]
    return render(request, 'index.html', locals())


# 自定义404和500的视图函数
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def page_error(request):
    return render(request, '404.html', status=500)
