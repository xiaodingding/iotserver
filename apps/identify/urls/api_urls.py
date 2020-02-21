#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter
# from django.urls import path, re_path
from .. import api

app_name = 'identify'

router = BulkRouter()
router.register(r'v1/identify', api.IdentifyViewSet, 'identify')


urlpatterns = [
     url(r'^v1/identify/token/$', api.IdentifyToken.as_view(), name='identify-token'),
     url(r'^v1/identify/image/$', api.ImageIdentifyAPI.as_view(), name='identify-image'),
]

urlpatterns += router.urls

