from django import VERSION
from . import views

__all__ = ["urlpatterns"]

app_name = 'editor'


if  VERSION<(1,9):
    from django.conf.urls import patterns, url
    urlpatterns = patterns('',
        url(r'^uploadimage/$', views.upload_image),
    )
else:
    from django.conf.urls import  url
    urlpatterns=[
        url(r'^uploadimage/$', views.upload_image,name='uploadimage'),
    ]
