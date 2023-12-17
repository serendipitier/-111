from django.urls import path
from .views import *
urlpatterns = [
    path('', loginView, name='login'),
    path('home/<int:page>.html', homeView, name='home'),
    path('logout.html', logoutView, name='logout'),
    path('upload.html', uploadView, name='upload')
]
