from django.shortcuts import render
from index.models import *
from user.models import MyUser


def rankingView(request):
    if request.user.username:
        uname = request.user.username
        this_user = MyUser.objects.get(username=uname).is_secert
    else:
        this_user=0
    searchs = Dynamic.objects.select_related('document').order_by('-search').all()[:4]
    labels = Label.objects.all()
    t = request.GET.get('type', '')
    if t:
        if this_user:
            dynamics = Dynamic.objects.select_related('document').filter(document__label=t).order_by('-plays').all()[:10]
        else:
            dynamics = Dynamic.objects.select_related('document').filter(document__label=t).filter(document_id__Classification=this_user).order_by('-plays').all()[:10]
    else:
        if this_user:
            dynamics = Dynamic.objects.select_related('document').order_by('-plays').all()[:10]
        else:
            dynamics = Dynamic.objects.select_related('document').filter(document_id__Classification=this_user).order_by('-plays').all()[:10]
    return render(request, 'ranking.html', locals())


from django.views.generic import ListView
class RankingList(ListView):
    context_object_name = 'dynamics'
    template_name = 'ranking.html'

    def get_queryset(self):
        t = self.request.GET.get('type', '')
        if t:
            dynamics = Dynamic.objects.select_related('document').filter(document__label=t).order_by('-plays').all()[:10]
        else:
            dynamics = Dynamic.objects.select_related('document').order_by('-plays').all()[:10]
        return dynamics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchs'] = Dynamic.objects.select_related('document').order_by('-search').all()[:4]
        context['labels'] = Label.objects.all()
        return context
