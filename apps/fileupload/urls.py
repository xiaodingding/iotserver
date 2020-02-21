# encoding: utf-8
from django import VERSION
from . import views


__all__ = ["urlpatterns"]

app_name = 'fileupload'




if  VERSION<(1,9):
    from django.conf.urls import patterns, url
    urlpatterns = patterns('',
       url('new/', views.PictureCreateView.as_view(), name='upload-new'),
       url('delete/(?P<pk>[0-9]+)/', views.PictureDeleteView.as_view(), name='upload-delete'),
       url('view/', views.PictureListView.as_view(), name='upload-view'),
       url('detail/(?P<pk>[0-9]+)/', views.PictureDetailView.as_view(), name='upload-detail'),
    )
else:
    from django.conf.urls import  url
    urlpatterns = [
        url('new/', views.PictureCreateView.as_view(), name='upload-new'),
        url('delete/(?P<pk>[0-9]+)/', views.PictureDeleteView.as_view(), name='upload-delete'),
        url('view/', views.PictureListView.as_view(), name='upload-view'),
        url('detail/(?P<pk>[0-9]+)/', views.PictureDetailView.as_view(), name='upload-detail'),
    ]
