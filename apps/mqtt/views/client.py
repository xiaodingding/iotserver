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


class ClientCreateView(AdminUserRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mqtt/client_create_update.html'
    success_url = reverse_lazy('mqtt:client-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Client'),
            'action': _('create client'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        client = form.save()
        #device.device_ico = self.request.GET['']
        client.created_by = self.request.user.username or 'System'
        client.user = self.request.user
        client.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mqtt/client_create_update.html'
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

