#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter
# from django.urls import path, re_path
from .. import api

app_name = 'nav'

router = BulkRouter()
router.register(r'v1/site', api.SiteViewSet, 'site')
router.register(r'v1/siteinfo', api.SiteInfoViewSet, 'siteinfo')
router.register(r'v1/category', api.CategoryViewSet, 'category')


urlpatterns = [
    url(r'^cad/$', api.CategoryListAsTreeApi.as_view(), name='all_category-site-list'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/site/$', api.CategorySiteViewSet.as_view(), name='silgle-category-site'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/child/$', api.CategoryViewSet, name='silgle-category-child'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/add/$', api.CategoryViewSet, name='category-add-children'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/site/add$', api.CategoryViewSet, name='category-site-add'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/site/replace$', api.CategoryViewSet, name='category-site-replace'),
]

urlpatterns += router.urls

