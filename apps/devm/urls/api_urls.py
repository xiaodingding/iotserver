# coding:utf-8
from django.conf.urls import url
from .. import api
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter

app_name = 'devm'


router = BulkRouter()

router.register(r'v1/device', api.DeviceViewSet, 'device')
router.register(r'v1/groups', api.DeviceGroupViewSet, 'device-group')
router.register(r'v1/datatp', api.DataTpViewSet, 'data-templet')
router.register(r'v1/datapoint', api.DataPointViewSet, 'data-point')
router.register(r'v1/data', api.DataViewSet, 'data-list')

urlpatterns = [
    url(r'^v1/data/reg/', api.DeviceTokenApi, name='data-reg'),
    url(r'^v1/data/data/', api.DeviceDataUpdate, name='data-status'),
    url(r'^v1/data/event/', api.DeviceDataUpdate, name='data-event'),
    url(r'^v1/data/latest$', api.DataLatestView, name='data-latest'),
    url(r'^v1/data/history$', api.DataHistoryView, name='data-history')
]

urlpatterns += router.urls

