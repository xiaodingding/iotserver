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
from mqtt.models.publisher import Server
from mqtt.forms import ServerForm



__all__ = [
    "ServerListView", "ServerUpdateView", "ServerDetailView",
    "ServerDeleteView"
]


class ServerListView(AdminUserRequiredMixin, ListView):
    model = Server
    template_name = 'mqtt/server_list.html'
    form_class = ServerForm

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Server'),
            'action': _('Server list'),
            'form': self.form_class()
        })
        return context


class ServerUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'mqtt/server_update.html'
    success_url = reverse_lazy('server:server-list')

    def get_context_data(self, **kwargs):
        context = super(ServerUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('Server'), 'action': _('Update server')})
        return context


class ServerDetailView(AdminUserRequiredMixin, DetailView):
    model = Server
    template_name = 'mqtt/server_detail.html'
    context_object_name = 'server'

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Server'),
            'action': _('Server detail')
        })
        return context


class ServerDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Server
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('server:server-list')

