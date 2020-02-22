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
from mqtt.models.publisher import  SecureConf
from mqtt.forms import  SecureConfForm



__all__ = [
    " SecureConfListView", " SecureConfUpdateView", " SecureConfDetailView",
    " SecureConfDeleteView"
]


class  SecureConfListView(AdminUserRequiredMixin, ListView):
    model =  SecureConf
    template_name = 'mqtt/scureconf_list.html'
    form_class =  SecureConfForm

    def get_context_data(self, **kwargs):
        context = super( SecureConfListView, self).get_context_data(**kwargs)
        context.update({
            'app': _(' SecureConf'),
            'action': _(' SecureConf list'),
            'form': self.form_class()
        })
        return context


class  SecureConfUpdateView(AdminUserRequiredMixin, UpdateView):
    model =  SecureConf
    form_class =  SecureConfForm
    template_name = 'mqtt/scureconf_update.html'
    success_url = reverse_lazy('scureconf:scureconf-list')

    def get_context_data(self, **kwargs):
        context = super( SecureConfUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _(' SecureConf'), 'action': _('Update scureconf')})
        return context


class  SecureConfDetailView(AdminUserRequiredMixin, DetailView):
    model =  SecureConf
    template_name = 'mqtt/scureconf_detail.html'
    context_object_name = 'scureconf'

    def get_context_data(self, **kwargs):
        context = super( SecureConfDetailView, self).get_context_data(**kwargs)
        context.update({
            'app': _(' SecureConf'),
            'action': _(' SecureConf detail')
        })
        return context


class  SecureConfDeleteView(AdminUserRequiredMixin, DeleteView):
    model =  SecureConf
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('scureconf:scureconf-list')

