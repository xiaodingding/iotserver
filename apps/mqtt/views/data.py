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
from mqtt.models.publisher import Data
from mqtt.forms import DataForm



__all__ = [
    "DataListView", "DataUpdateView", "DataDetailView",
    "DataDeleteView"
]


class DataListView(AdminUserRequiredMixin, ListView):
    model = Data
    template_name = 'mqtt/data_list.html'
    form_class = DataForm

    def get_context_data(self, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Data'),
            'action': _('Data list'),
            'form': self.form_class()
        })
        return context


class DataCreateView(AdminUserRequiredMixin, CreateView):
    model = Data
    form_class = DataForm
    template_name = 'mqtt/data_create_update.html'
    success_url = reverse_lazy('mqtt:data-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Data'),
            'action': _('data server'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        server = form.save()
        server.created_by = self.request.user.username or 'System'
        server.save()
        return super(DataCreateView, self).form_valid(form)


class DataUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Data
    form_class = DataForm
    template_name = 'mqtt/data_create_update.html'
    success_url = reverse_lazy('mqtt:data-list')

    def get_context_data(self, **kwargs):
        context = super(DataUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('Data'), 'action': _('Update data')})
        return context


class DataDetailView(AdminUserRequiredMixin, DetailView):
    model = Data
    template_name = 'mqtt/data_detail.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(DataDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Data'),
            'action': _('Data detail')
        })
        return context


class DataDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Data
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('data:data-list')

