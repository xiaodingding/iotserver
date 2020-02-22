#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from rest_framework import routers

from .. import api

app_name = 'mqtt'

router = routers.DefaultRouter()
router.register(r'v1/auth', api.AuthViewSet, 'auth')
router.register(r'v1/client', api.ClientViewSet, 'client')
router.register(r'v1/secure', api.SecureViewSet, 'secure')
router.register(r'v1/server', api.ServerViewSet, 'server')

urlpatterns = [

]

urlpatterns += router.urls
