# coding:utf-8

from __future__ import unicode_literals


from django.conf.urls import url
from ..views import category, site, nav, siteinfo
# from ..views import site
# from ..views import nav

app_name = 'nav'

urlpatterns = [
    # nav

    url(r'^index$', nav.NavIndexView.as_view(), name='index'),
    url(r'^about$', nav.NavAboutView.as_view(), name='about'),

    url(r'^nav$', category.CategoryAndSitesListView.as_view(), name='category-site-list'),
    url(r'^category/$', category.CategoryListView.as_view(), name='category-list'),
    url(r'^category/create/$', category.CategoryCreateView.as_view(), name='category-create'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', category.CategoryUpdateView.as_view(), name='category-update'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/$', category.CategoryDetailView.as_view(), name='category-detail'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', category.CategoryDeleteView.as_view(), name='category-delete'),
    url(r'^category/(?P<pk>[0-9a-zA-Z\-]{36})/user/$', category.CategoryUserView.as_view(), name='category-user-list'),


    url(r'^site/$', site.SiteListView.as_view(), name='site-list'),
    url(r'^site/create/$', site.SiteCreateView.as_view(), name='site-create'),
    url(r'^site/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', site.SiteUpdateView.as_view(), name='site-update'),
    url(r'^site/(?P<pk>[0-9a-zA-Z\-]{36})/$', site.SiteDetailView.as_view(), name='site-detail'),
    url(r'^site/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', site.SiteDeleteView.as_view(), name='site-delete'),


    url(r'^siteinfo/$', siteinfo.SiteInfoListView.as_view(), name='siteinfo-list'),
    url(r'^siteinfo/create/$', siteinfo.SiteInfoCreateView.as_view(), name='siteinfo-create'),
    url(r'^siteinfo/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', siteinfo.SiteInfoUpdateView.as_view(), name='siteinfo-update'),
    url(r'^siteinfo/(?P<pk>[0-9a-zA-Z\-]{36})/$', siteinfo.SiteInfoDetailView.as_view(), name='siteinfo-detail'),
    url(r'^siteinfo/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', siteinfo.SiteInfoDeleteView.as_view(), name='siteinfo-delete')
]
