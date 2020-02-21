# coding:utf-8
from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import get_object_or_404, reverse, redirect

from .. import forms
from ..models.datapoint import DataPoint
from ..models.group import DeviceGroup
from ..models.datatemplet import DataTemplet
from ..models.device import Device

from ..hands import AdminUserRequiredMixin


__all__ = ['DeviceGroupCreateView', 'DeviceGroupDetailView',
           'DeviceGroupUpdateView', 'DeviceGroupListView',
           'DeviceGroupDeleteView',
           ]


class DeviceGroupCreateView(AdminUserRequiredMixin, CreateView):
    model = DeviceGroup
    form_class = forms.DeviceGroupForm
    template_name = 'devm/device_group_create.html'
    success_url = reverse_lazy('devm:device-group-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devices'),
            'action': _('Create Device Group'),
            'devices_count': 0,
        }
        kwargs.update(context)
        return super(DeviceGroupCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        device_group = form.save()
        devices_id_list = self.request.POST.getlist('devices', [])
        devices = [get_object_or_404(Device, id=int(device_id))
                  for device_id in devices_id_list]
        device_group.created_by = self.request.user.username or 'Admin'
        device_group.devices.add(*tuple(devices))
        device_group.save()
        return super(DeviceGroupCreateView, self).form_valid(form)


class DeviceGroupListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devm/device_group_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Device Group List'),
            'devices': Device.objects.all(),
            # 'system_users': SystemUser.objects.all(),
            'keyword': self.request.GET.get('keyword', '')
        }
        kwargs.update(context)
        return super(DeviceGroupListView, self).get_context_data(**kwargs)


class DeviceGroupDetailView(AdminUserRequiredMixin, DetailView):
    model = DeviceGroup
    template_name = 'devm/device_group_detail.html'
    context_object_name = 'device_group'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Device Group Detail'),
        }
        kwargs.update(context)
        return super(DeviceGroupDetailView, self).get_context_data(**kwargs)


class DeviceGroupUpdateView(AdminUserRequiredMixin, UpdateView):
    model = DeviceGroup
    form_class = forms.DeviceGroupForm
    template_name = 'devm/device_group_create.html'
    success_url = reverse_lazy('devm:device-group-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=DeviceGroup.objects.all())
        return super(DeviceGroupUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        devices_all = Device.objects.filter(groups=self.object.id).all()
        context = {
            'app': _('Devices'),
            'action': _('Update Device Group'),
            'devices_on_list': devices_all,
            'devices_count': len(devices_all),
            'group_id': self.object.id,
        }
        kwargs.update(context)
        return super(DeviceGroupUpdateView, self).get_context_data(**kwargs)


class DeviceGroupDeleteView(AdminUserRequiredMixin, DeleteView):
    template_name = 'devm/delete_confirm.html'
    model = DeviceGroup
    success_url = reverse_lazy('devm:device-group-list')
