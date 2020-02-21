# coding:utf-8

from __future__ import unicode_literals


from django.conf.urls import url
from ..views import identify


app_name = 'identify'

urlpatterns = [
    # identify

    url(r'^identify/$', identify.IdentifyListView.as_view(), name='identify-list'),
    url(r'^identify/create/$', identify.IdentifyCreateView.as_view(), name='identify-create'),
    url(r'^identify/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', identify.IdentifyUpdateView.as_view(), name='identify-update'),
    url(r'^identify/(?P<pk>[0-9a-zA-Z\-]{36})/$', identify.IdentifyDetailView.as_view(), name='identify-detail'),
    url(r'^identify/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', identify.IdentifyDeleteView.as_view(), name='identify-delete'),
    url(r'^identify/(?P<pk>[0-9a-zA-Z\-]{36})/user/$', identify.IdentifyUserView.as_view(), name='identify-user-list'),

]
