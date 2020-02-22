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
from mqtt.models.publisher import Client
from mqtt.forms import ClientForm



__all__ = [
    "ClientListView", "ClientUpdateView", "ClientDetailView",
    "ClientDeleteView"
]


class ClientListView(AdminUserRequiredMixin, ListView):
    model = Client
    template_name = 'mqtt/client_list.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Client'),
            'action': _('Client list'),
            'form': self.form_class()
        })
        return context


class ClientUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mqtt/client_update.html'
    success_url = reverse_lazy('client:client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('Client'), 'action': _('Update client')})
        return context


class ClientDetailView(AdminUserRequiredMixin, DetailView):
    model = Client
    template_name = 'mqtt/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Client'),
            'action': _('Client detail')
        })
        return context


class ClientDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Client
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('client:client-list')

