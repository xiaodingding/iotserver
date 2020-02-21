# coding:utf-8
from __future__ import absolute_import, unicode_literals
import uuid

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.conf import settings

from .. import forms
from ..models.datapoint import DataPoint
from ..models.group import DeviceGroup
from ..models.datatemplet import DataTemplet
from ..models.device import Device
from ..models.data import Data
from ..hands import AdminUserRequiredMixin
from ..utils import device_point_query




__all__ = ['DeviceListView', 'DeviceCreateView', 'DeviceUpdateView',
           'DeviceDetailView', 'DeviceDeleteView', 'DeviceModalListView',
           'DeviceDataHistoryView']


class DeviceListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devm/device_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Device list'),
            # 'keyword': self.request.GET.get('keyword', '')
        }
        kwargs.update(context)
        return super(DeviceListView, self).get_context_data(**kwargs)


class DeviceCreateView(AdminUserRequiredMixin, CreateView):
    model = Device
    form_class = forms.DeviceCreateForm
    template_name = 'devm/device_create.html'
    success_url = reverse_lazy('devm:device-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Create Device'),
        }
        kwargs.update(context)
        return super(DeviceCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        device = form.save()
        #device.device_ico = self.request.GET['']
        device.created_by = self.request.user.username or 'System'
        device.save()
        return super(DeviceCreateView, self).form_valid(form)


class DeviceUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Device
    form_class = forms.DeviceCreateForm #forms.DeviceForm
    template_name = 'devm/device_create.html'
    context_object_name = 'devm'
    success_url = reverse_lazy('devm:device-list')

    def form_valid(self, form):
        devm = form.save(commit=False)
        #print(self.request.GET['id_device_ico'])
        devm.save()
        return super(DeviceUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        device = self.model.objects.get(id=self.object.pk)

        print(device.device_ico)
        context = {
            'app': _('Devm'),
            'action': _('Update Device'),
            'device':device,
        }
        kwargs.update(context)
        return super(DeviceUpdateView, self).get_context_data(**kwargs)



class DeviceDetailView(AdminUserRequiredMixin, DetailView):
    model = Device
    template_name = 'devm/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        print(self.object.name)
        templet = self.object.datatemplet.all()[:1]
        dtpoint = device_point_query(self.object)
        legend = ""
        data_point_nbr = 0

        if((len(templet) < 1) or dtpoint is None):
            pass
        else:
            if(len(dtpoint) > 0):
                data = Data.objects.filter(device= self.object).all()[:1]
                if(len(data) > 0):
                    data = data[0].data_content.split(";")
                    # print(data)
                else:
                    data = []
                if(len(data) < len(dtpoint)):
                    for i in range(len(data),(len(dtpoint))):
                        data.append('0')
                i = 0
                for key in dtpoint:
                    if i < 1:
                        legend = "'" + key.name + "(" + key.data_uint + ")'"
                    else:
                        legend = legend + ",'" + key.name + "(" + key.data_uint + ")'"
                    setattr(key,"value",data[i])
                    setattr(key, "nbr", i+1)
                    i = i + 1

        print(legend)
        context = {
            'app': _('Devm'),
            'action': _('Update Device'),
            'datapoint':dtpoint,
            'chart_legend':legend,
            'data_point_total':len(dtpoint)
        }
        kwargs.update(context)
        return super(DeviceDetailView, self).get_context_data(**kwargs)

class DeviceDataHistoryView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devm/device_data.html'

    def get_context_data(self, **kwargs):
        device_id = self.request.GET.get('id')
        point_id = self.request.GET.get('data_point')
        # print("device: %s" % device_id)
        device = Device.objects.filter(id = device_id)[:1]
        device = device[0]
        datapoint = DataPoint.objects.filter(id=point_id)[:1]
        context = {
            'app': _('Devm'),
            'action': _('Device Data History'),
            'device':device,
            'datapoint':datapoint[0],
            'data_point_nbr':point_id
        }
        kwargs.update(context)
        return super(DeviceDataHistoryView, self).get_context_data(**kwargs)

class DeviceDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Device
    template_name = 'devm/delete_confirm.html'
    success_url = reverse_lazy('devm:device-list')


class DeviceModalListView(AdminUserRequiredMixin, ListView):
    paginate_by = settings.CONFIG.DISPLAY_PER_PAGE
    model = Device
    context_object_name = 'device_modal_list'
    template_name = 'devm/device_modal_list.html'

    def get_context_data(self, **kwargs):
        devices = Device.objects.all()
        device_id = self.request.GET.get('device_id', '')
        device_id_list = [i for i in device_id.split(',') if i.isdigit()]
        context = {
            'all_device': device_id_list,
            'devices': devices,
        }
        kwargs.update(context)
        return super(DeviceModalListView, self).get_context_data(**kwargs)

