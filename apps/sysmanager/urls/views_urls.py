from __future__ import absolute_import

from django.conf.urls import url

from ..views import notice

app_name = 'sysmanager'

urlpatterns = [
    # 公告
    url(r'^notice/$', notice.NoticeListView.as_view(), name='notice-list'),
    url(r'^notice/(?P<pk>[0-9a-zA-Z\-]{36})$', notice.NoticeDetailView.as_view(), name='notice-detail'),
    url(r'^notice/create$', notice.NoticeCreateView.as_view(), name='notice-create'),
    url(r'^notice/(?P<pk>[0-9a-zA-Z\-]{36})/update$', notice.NoticeUpdateView.as_view(), name='notice-update'),
    url(r'^notice/last$', notice.NoticeGetLastView, name='notice-last'),
]
