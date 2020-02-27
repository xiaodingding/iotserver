# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .views import IndexView

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^users/', include('users.urls.views_urls', namespace='users')),
    url(r'^ops/', include('ops.urls.view_urls', namespace='ops')),
    url(r'^settings/', include('common.urls.view_urls', namespace='settings')),
    url(r'^common/', include('common.urls.view_urls', namespace='common')),
    url(r'^terminal/', include('terminal.urls.views_urls', namespace='terminal')),
    url(r'^devm/', include('devm.urls.views_urls', namespace='devm')),
    url(r'^sysmanager/', include('sysmanager.urls.views_urls', namespace='sysmanager')),
    url(r'^mqtt/', include('mqtt.urls.views_urls', namespace='mqtt')),

    #多媒体相关
    url(r'^editor/', include('editor.urls', namespace='editor')),
    url(r'^ueditor/', include('ueditor.urls', namespace='ueditor')),
    url(r'upload/', include('fileupload.urls', namespace='fileupload')),

    # Api url view map
    url(r'^api/users/', include('users.urls.api_urls', namespace='api-users')),
    url(r'^api/ops/', include('ops.urls.api_urls', namespace='api-ops')),
    url(r'^api/common/', include('common.urls.api_urls', namespace='api-common')),
    url(r'^api/terminal/', include('terminal.urls.api_urls', namespace='api-terminal')),
    url(r'^api/devm/', include('devm.urls.api_urls', namespace='api-devm')),
    url(r'^api/nav/', include('nav.urls.api_urls', namespace='api-nav')),
    url(r'^api/sysmanager/', include('sysmanager.urls.api_urls', namespace='api-sysmanager')),
    url(r'^api/identify/', include('identify.urls.api_urls', namespace='api-identify')),
    url(r'^api/mqtt/', include('mqtt.urls.api_urls', namespace='api-mqtt')),

    # External apps url
    url(r'^captcha/', include('captcha.urls')),



    # tinymce
    #url(r'^tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^docs/', schema_view, name="docs"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

