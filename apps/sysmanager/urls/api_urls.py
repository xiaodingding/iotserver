#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter
from .. import api

app_name = 'sysmanager'

router = BulkRouter()
router.register(r'v1/notice', api.NoticeViewSet, 'notice')
#router.register(r'v1/groups', api.UserGroupViewSet, 'user-group')


urlpatterns = [
    # url(r'', api.UserListView.as_view()),
    #url(r'^v1/token/$', api.UserToken.as_view(), name='user-token'),
]

urlpatterns += router.urls
