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
from mqtt.models.publisher import SecureConf
from mqtt.forms import SecureConfForm



__all__ = [
    "SecureConfListView", "SecureConfUpdateView", "SecureConfDetailView",
    "SecureConfDeleteView"
]


class SecureConfListView(AdminUserRequiredMixin, ListView):
    model = SecureConf
    template_name = 'mqtt/secure_list.html'
    form_class = SecureConfForm

    def get_context_data(self, **kwargs):
        context = super(SecureConfListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('SecureConf'),
            'action': _('SecureConf list'),
            'form': self.form_class()
        })
        return context


class SecureConfCreateView(AdminUserRequiredMixin, CreateView):
    model = SecureConf
    form_class = SecureConfForm
    template_name = 'mqtt/secure_create_update.html'
    success_url = reverse_lazy('mqtt:secure-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('SecureConf'),
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
        return super(SecureConfCreateView, self).form_valid(form)


class SecureConfUpdateView(AdminUserRequiredMixin, UpdateView):
    model = SecureConf
    form_class = SecureConfForm
    template_name = 'mqtt/secure_update.html'
    success_url = reverse_lazy('secure:secure-list')

    def get_context_data(self, **kwargs):
        context = super(SecureConfUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('SecureConf'), 'action': _('Update secure')})
        return context


class SecureConfDetailView(AdminUserRequiredMixin, DetailView):
    model = SecureConf
    template_name = 'mqtt/secure_detail.html'
    context_object_name = 'secure'

    def get_context_data(self, **kwargs):
        context = super(SecureConfDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _('SecureConf'),
            'action': _('SecureConf detail')
        })
        return context


class SecureConfDeleteView(AdminUserRequiredMixin, DeleteView):
    model = SecureConf
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('secure:secure-list')

