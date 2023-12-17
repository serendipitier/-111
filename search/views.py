from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import reverse
from django.db.models import Q, F
from index.models import *
from user.models import MyUser


def searchView(request, page):
    if request.method == 'GET':
        if request.user.username:
            uname = request.user.username
            this_user = MyUser.objects.get(username=uname).is_secert
        else:
            this_user = 0
        searchs = Dynamic.objects.select_related('document').order_by('-search').all()[:6]
        kword = request.session.get('kword', '')
        if kword:
            if this_user:
                Documents = Document.objects.filter(Q(name__icontains=kword) | Q(person=kword)).order_by('-time').all()
            else:
                Documents = Document.objects.filter(Q(name__icontains=kword) | Q(person=kword)).filter(Classification=this_user).order_by('-time').all()
        else:
            if this_user:
                Documents = Document.objects.order_by('-time').all()[:50]
            else:
                Documents = Document.objects.filter(Classification=this_user).order_by('-time').all()[:50]
        paginator = Paginator(Documents, 7)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        if kword:
            idList = Document.objects.filter(name__icontains=kword)
            for i in idList:
                dynamics = Dynamic.objects.filter(document_id=i.id)
                if dynamics:
                    dynamics.update(search=F('search') + 1)
                else:
                    dynamic = Dynamic(plays=0, search=1, download=0, Document_id=i.id)
                    dynamic.save()
        return render(request, 'search.html', locals())
    else:
        request.session['kword'] = request.POST.get('kword', '')
        return redirect(reverse('search', kwargs={'page': 1}))