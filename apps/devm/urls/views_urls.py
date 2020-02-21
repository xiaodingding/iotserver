# coding:utf-8
from django.conf.urls import url
from .. import views

app_name = 'devm'

urlpatterns = [
    # Resource device url
    url(r'^device/$', views.DeviceListView.as_view(), name='device-list'),
    url(r'^device/create/$', views.DeviceCreateView.as_view(), name='device-create'),
    url(r'^device/(?P<pk>[0-9]+)/$', views.DeviceDetailView.as_view(), name='device-detail'),
    url(r'^device/(?P<pk>[0-9]+)/update/$', views.DeviceUpdateView.as_view(), name='device-update'),
    url(r'^device/(?P<pk>[0-9]+)/delete/$', views.DeviceDeleteView.as_view(), name='device-delete'),
    url(r'^device-modal$', views.DeviceModalListView.as_view(), name='device-modal-list'),
    url(r'^device-history$', views.DeviceDataHistoryView.as_view(), name='device-data-history'),
    #url(r'^device/(?P<pk>[0-9]+)/assets/$', views.IDCAssetsView.as_view(), name='device-assets'),

    # Resource device group url
    url(r'^device-group/$', views.DeviceGroupListView.as_view(), name='device-group-list'),
    url(r'^device-group/create/$', views.DeviceGroupCreateView.as_view(), name='device-group-create'),
    url(r'^device-group/(?P<pk>[0-9]+)/$', views.DeviceGroupDetailView.as_view(), name='device-group-detail'),
    url(r'^device-group/(?P<pk>[0-9]+)/update/$', views.DeviceGroupUpdateView.as_view(), name='device-group-update'),
    url(r'^device-group/(?P<pk>[0-9]+)/delete/$', views.DeviceGroupDeleteView.as_view(), name='device-group-delete'),

    # Resource data templet url
    url(r'^data-templet/$', views.DataTptListView.as_view(), name='data-templet-list'),
    url(r'^data-templet/create/$', views.DataTptCreateView.as_view(), name='data-templet-create'),
    url(r'^data-templet/(?P<pk>[0-9]+)/$', views.DataTptDetailView.as_view(), name='data-templet-detail'),
    url(r'^data-templet/(?P<pk>[0-9]+)/update/$', views.DataTptUpdateView.as_view(), name='data-templet-update'),
    url(r'^data-templet/(?P<pk>[0-9]+)/delete/$', views.DataTptDeleteView.as_view(), name='data-templet-delete'),

    # Resource data templet url
    url(r'^data-point/$', views.DataPointListView.as_view(), name='data-point-list'),
    url(r'^data-point/create$', views.DataPointCreateView.as_view(), name='data-point-create'),
    url(r'^data-point/modal/(?P<pk>[0-9]+)/$', views.DataPointModalView.as_view(), name='data-point-modal'),
    url(r'^data-point/(?P<pk>[0-9]+)/$', views.DataPointDetailView.as_view(), name='data-point-detail'),
    url(r'^data-point/(?P<pk>[0-9]+)/update$', views.DataPointUpdateView.as_view(), name='data-point-update'),
    url(r'^data-point/(?P<pk>[0-9]+)/delete/$', views.DataPointDeleteView.as_view(), name='data-point-delete'),
]

