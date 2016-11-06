from django.conf.urls import url,include
from django.contrib import admin
from .views import *

urlpatterns = [
   
    url(r'^create/$',posts_create),
    url(r'^(?P<id>\d+)/$',posts_detail , name='detail'),
    url(r'^list/$',posts_list,name='list'),
    url(r'^(?P<id>\d+)/edit/$',posts_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$',posts_delete),


]
