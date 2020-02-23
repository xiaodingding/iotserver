#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'mqtt'

router = BulkRouter()
router.register(r'v1/auth',   api.AuthViewSet,   'auth')
router.register(r'v1/client', api.ClientViewSet, 'client')
router.register(r'v1/secure', api.SecureViewSet, 'secure')
router.register(r'v1/server', api.ServerViewSet, 'server')
router.register(r'v1/data',   api.DataViewSet,   'data')
router.register(r'v1/topic',  api.TopicViewSet,  'topic')

urlpatterns = [
    # url(r'^v1/auth/image/$', api.AuthViewSet.as_view(), name='identify-image'),
    # url(r'^v1/client_list/$', api.ClientListAPI.as_view(), name='client-all-list'),
]

urlpatterns += router.urls
