# coding:utf-8
from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import reverse, redirect
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.conf import settings
from django.forms.models import model_to_dict

from .. import forms
from ..models.datapoint import DataPoint
from ..models.group import DeviceGroup
from ..models.datatemplet import DataTemplet
from ..models.device import Device

from ..hands import AdminUserRequiredMixin


__all__ = ['DataPointListView', 'DataPointCreateView', 'DataPointUpdateView',
           'DataPointDetailView', 'DataPointDeleteView', 'DataPointModalView']


class DataPointListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devm/device_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('DataPoint list'),
            # 'keyword': self.request.GET.get('keyword', '')
        }
        kwargs.update(context)
        return super(DataPointListView, self).get_context_data(**kwargs)


class DataPointCreateView(AdminUserRequiredMixin, CreateView):
    model = DataPoint
    form_class = forms.DataPointCreateForm
    template_name = 'devm/data_point_create.html'
    success_url = reverse_lazy('devm:data-templet-detail')


    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Create Data Point'),
        }

        kwargs.update(context)
        return super(DataPointCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        device = form.save()
        device.created_by = self.request.user.username or 'System'
        device.save()
        return super(DataPointCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('devm:data-templet-detail',
                       kwargs={'pk': self.request.GET.get('templet_id')})

class DataPointUpdateView(AdminUserRequiredMixin, UpdateView):
    model = DataPoint
    form_class = forms.DataPointCreateForm
    template_name = 'devm/data_point_create.html'
    context_object_name = 'datapoint'
    success_url = reverse_lazy('devm:data-templet-detail')

    def form_valid(self, form):
        devm = form.save(commit=False)
        devm.save()
        return super(DataPointUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Update DataPoint'),
        }
        kwargs.update(context)
        return super(DataPointUpdateView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('devm:data-templet-detail',
                       kwargs={'pk': self.request.GET.get('templet_id')})


class DataPointDetailView(AdminUserRequiredMixin, DetailView):
    model = DataPoint
    template_name = 'devm/data_point_detail.html'
    context_object_name = 'datapoint'


class DataPointModalView(AdminUserRequiredMixin, DetailView):
    model = DataPoint
    template_name = 'devm/_data_point_show_modal.html'
    #context_object_name = 'datapoint'

    def get_context_data(self, **kwargs):
        print(self.object.pk)
        dt = DataPoint.objects.filter(id=self.object.pk).all()

        context = {
            'app': _('Devm'),
            'action': _('device group detail'),
            'datapoint':dt[0]
        }
        kwargs.update(context)
        return super(DataPointModalView, self).get_context_data(**kwargs)

class DataPointDeleteView(AdminUserRequiredMixin, DeleteView):
    model = DataPoint
    template_name = 'devm/delete_confirm.html'
    success_url = reverse_lazy('devm:device-list')

