#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.conf.urls import url

from .. import views

app_name = 'mqtt'

urlpatterns = [
    # Server view
    url(r'^server/$', views.severs.ServerListView.as_view(), name='server-list'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.severs.ServerDetailView.as_view(), name='server-detail'),
    # url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/connect/$', views.severs.ServerConnectView.as_view(), name='server-connect'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.severs.ServerUpdateView.as_view(), name='server-update'),
    url(r'^server/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.severs.ServerDeleteView.as_view(), name='server-delete'),

    # Client view
    url(r'^client/$', views.client.ClientListView.as_view(), name='client-list'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.client.ClientDetailView.as_view(), name='client-detail'),
    # url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/connect/$', views.client.ClientConnectView.as_view(), name='client-connect'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.client.ClientUpdateView.as_view(), name='client-update'),
    url(r'^client/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.client.ClientDeleteView.as_view(), name='client-delete'),

    # Secure view
    url(r'^secure/$', views.secure.SecureConfListView.as_view(), name='secure-list'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.secure.SecureConfDetailView.as_view(), name='secure-detail'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.secure.SecureConfUpdateView.as_view(), name='secure-update'),
    url(r'^secure/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.secure.SecureConfDeleteView.as_view(), name='secure-delete'),


]
