# -*- coding: utf-8 -*-
#

from django.views.generic import ListView, UpdateView, DeleteView, \
    DetailView, CreateView
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


class ServerCreateView(AdminUserRequiredMixin, CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'mqtt/server_create_update.html'
    success_url = reverse_lazy('mqtt:server-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Server'),
            'action': _('create server'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        server = form.save()
        #device.device_ico = self.request.GET['']
        server.created_by = self.request.user.username or 'System'
        server.user = self.request.user
        server.save()
        return super(ServerCreateView, self).form_valid(form)


class ServerUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'mqtt/server_create_update.html'
    success_url = reverse_lazy('mqtt:server-list')

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

