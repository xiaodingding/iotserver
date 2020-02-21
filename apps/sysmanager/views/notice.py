# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals

import json
import uuid
import csv
import codecs
from io import StringIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView, FormMixin, FormView
)
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout

from common.const import create_success_msg, update_success_msg


from .. import forms
from ..models import Notice
from ..hands import AdminUserRequiredMixin



__all__ = [
    'NoticeListView', 'NoticeCreateView', 'NoticeDetailView',
    'NoticeUpdateView',
]

#logger = get_logger(__name__)


class NoticeListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'sysmanager/notice_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Notices'),
            'action': _('Notices List'),
            'keyword': self.request.GET.get('keyword', '')
        }
        kwargs.update(context)
        return super(NoticeListView, self).get_context_data(**kwargs)


class NoticeCreateView(AdminUserRequiredMixin, CreateView):
    model = Notice
    form_class = forms.NoticeForm
    template_name = 'sysmanager/notice_create.html'
    success_url = reverse_lazy('sysmanager:notice-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Notices'),
            'action': _('Create Notices'),
        }
        kwargs.update(context)
        return super(NoticeCreateView, self).get_context_data(**kwargs)


    def form_valid(self, form):
        notice = form.save()
        notice.created_by = self.request.user.username or 'System'
        print(notice)
        notice.save()
        return super(NoticeCreateView, self).form_valid(form)


class NoticeUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Notice
    form_class = forms.NoticeForm
    template_name = 'sysmanager/notice_create.html'
    context_object_name = 'notice_object'
    success_url = reverse_lazy('sysmanager:notice-list')


    def get_context_data(self, **kwargs):
        context = {'app': _('Notices'), 'action': _('Update Notice')}
        kwargs.update(context)
        return super().get_context_data(**kwargs)



class NoticeDetailView(AdminUserRequiredMixin, DetailView):
    model = Notice
    template_name = 'sysmanager/notice_detail.html'
    context_object_name = 'notice'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Notices'),
            'action': _('Notice detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

def NoticeGetLastView(request):
    notice = Notice.objects.last()
    news = {'title': notice.title, 'body': notice.body, 'created_by': notice.created_by,
            'date_created': (notice.date_created.strftime('%b-%d-%y %H:%M:%S'))}
    return HttpResponse(json.dumps(news), content_type="application/json")


