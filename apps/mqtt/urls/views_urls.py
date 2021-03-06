#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.conf.urls import url

from .. import views

app_name = 'mqtt'

urlpatterns = [
    # Server view
    url(r'^server/$', views.severs.ServerListView.as_view(), name='server-list'),
    url(r'^server/create/$', views.severs.ServerCreateView.as_view(), name='server-create'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.severs.ServerDetailView.as_view(), name='server-detail'),
    # url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/connect/$', views.severs.ServerConnectView.as_view(), name='server-connect'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.severs.ServerUpdateView.as_view(), name='server-update'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.severs.ServerDeleteView.as_view(), name='server-delete'),

    # Client view
    url(r'^client/$', views.client.ClientListView.as_view(), name='client-list'),
    url(r'^client/create/$', views.client.ClientCreateView.as_view(), name='client-create'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.client.ClientDetailView.as_view(), name='client-detail'),
    # url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/connect/$', views.client.ClientConnectView.as_view(), name='client-connect'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.client.ClientUpdateView.as_view(), name='client-update'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.client.ClientDeleteView.as_view(), name='client-delete'),

    # Secure view
    url(r'^secure/$', views.secure.SecureConfListView.as_view(), name='secure-list'),
    url(r'^secure/create/$', views.secure.SecureConfCreateView.as_view(), name='secure-create'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.secure.SecureConfDetailView.as_view(), name='secure-detail'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.secure.SecureConfUpdateView.as_view(), name='secure-update'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.secure.SecureConfDeleteView.as_view(), name='secure-delete'),


    # Auth view
    url(r'^auth/$', views.auth.AuthListView.as_view(), name='auth-list'),
    url(r'^auth/create/$', views.auth.AuthCreateView.as_view(), name='auth-create'),
    url(r'^auth/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.auth.AuthDetailView.as_view(), name='auth-detail'),
    url(r'^auth/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.auth.AuthUpdateView.as_view(), name='auth-update'),
    url(r'^auth/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.auth.AuthDeleteView.as_view(), name='auth-delete'),

    # Data view
    url(r'^data/$', views.data.DataListView.as_view(), name='data-list'),
    url(r'^data/create/$', views.data.DataCreateView.as_view(), name='data-create'),
    url(r'^data/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.data.DataDetailView.as_view(), name='data-detail'),
    url(r'^data/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.data.DataUpdateView.as_view(), name='data-update'),
    url(r'^data/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.data.DataDeleteView.as_view(), name='data-delete'),

    # Topic view
    url(r'^topic/$', views.topic.TopicListView.as_view(), name='topic-list'),
    url(r'^topic/create/$', views.topic.TopicCreateView.as_view(), name='topic-create'),
    url(r'^topic/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.topic.TopicDetailView.as_view(), name='topic-detail'),
    url(r'^topic/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.topic.TopicUpdateView.as_view(), name='topic-update'),
    url(r'^topic/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.topic.TopicDeleteView.as_view(), name='topic-delete'),
]
