# -*- coding: utf-8 -*-
#

from django.views.generic import ListView, UpdateView, DeleteView, \
    DetailView, View
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy, reverse

from users.utils import AdminUserRequiredMixin
from common.mixins import DatetimeSearchMixin
from mqtt.models.publisher import Auth
from mqtt.forms import AuthForm



__all__ = [
    "AuthListView", "AuthUpdateView", "AuthDetailView",
    "AuthDeleteView"
]


class AuthListView(AdminUserRequiredMixin, ListView):
    model = Auth
    template_name = 'mqtt/auth_list.html'
    form_class = AuthForm

    def get_context_data(self, **kwargs):
        context = super(AuthListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Auth'),
            'action': _('Auth list'),
            'form': self.form_class()
        })
        return context


class AuthUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Auth
    form_class = AuthForm
    template_name = 'mqtt/auth_update.html'
    success_url = reverse_lazy('auth:auth-list')

    def get_context_data(self, **kwargs):
        context = super(AuthUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('Auth'), 'action': _('Update auth')})
        return context


class AuthDetailView(AdminUserRequiredMixin, DetailView):
    model = Auth
    template_name = 'mqtt/auth_detail.html'
    context_object_name = 'auth'

    def get_context_data(self, **kwargs):
        context = super(AuthDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Auth'),
            'action': _('Auth detail')
        })
        return context


class AuthDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Auth
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('auth:auth-list')

