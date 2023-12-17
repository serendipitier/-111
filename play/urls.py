from django.urls import path
from .views import *
urlpatterns = [
    # 公文在线查看
    path('<int:id>.html', playView, name='play'),
    # 公文下载
    path('download/<int:id>.html', downloadView, name='download'),

    path('<int:id>.pdf', downloadr, name='downloadr')
]
