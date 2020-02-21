# coding:utf-8
from __future__ import absolute_import, unicode_literals
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

from ..hands import AdminUserRequiredMixin


__all__ = ['DataTptListView', 'DataTptCreateView', 'DataTptUpdateView',
           'DataTptDetailView', 'DataTptDeleteView', 'DataTptModalListView']


class DataTptListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'devm/data_templet_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('DataTemplet List'),
            # 'keyword': self.request.GET.get('keyword', '')
        }
        kwargs.update(context)
        return super(DataTptListView, self).get_context_data(**kwargs)


class DataTptCreateView(AdminUserRequiredMixin, CreateView):
    model = DataTemplet
    form_class = forms.DataTptCreateForm
    template_name = 'devm/data_templet_create.html'
    success_url = reverse_lazy('devm:data-templet-list')


    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Create DataTemplet'),
        }
        kwargs.update(context)
        return super(DataTptCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        device = form.save()
        device.created_by = self.request.user.username or 'System'
        device.save()
        return super(DataTptCreateView, self).form_valid(form)

    # def get_success_url(self):
    #     #update_assets_hardware_info.delay([self.asset._to_secret_json()])
    #     return super(DataTptCreateView, self).get_success_url()

class DataTptUpdateView(AdminUserRequiredMixin, UpdateView):
    model = DataTemplet
    form_class = forms.DataTptCreateForm
    template_name = 'devm/data_templet_create.html'
    context_object_name = 'devm'
    success_url = reverse_lazy('devm:data-templet-list')

    def form_valid(self, form):
        devm = form.save(commit=False)
        devm.save()
        return super(DataTptUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Devm'),
            'action': _('Update DataTemplet'),
        }
        kwargs.update(context)
        return super(DataTptUpdateView, self).get_context_data(**kwargs)


class DataTptDetailView(AdminUserRequiredMixin, DetailView):
    model = DataTemplet
    template_name = 'devm/data_templet_detail.html'
    context_object_name = 'data_templet'

    def get_context_data(self, **kwargs):
        # devices_remain = Device.objects.exclude(id__in=self.object.devices.all())
        # system_users = SystemUser.objects.all()
        # system_users_remain = SystemUser.objects.exclude(id__in=system_users)
        context = {
            'app': _('Devm'),
            'action': _('device group detail'),
            # 'devices_remain': devices_remain,
            # 'devices': [device for device in Device.objects.all()
            #            if device not in devices_remain],
            # 'system_users': system_users,
            # 'system_users_remain': system_users_remain,
        }
        kwargs.update(context)
        return super(DataTptDetailView, self).get_context_data(**kwargs)




class DataTptDeleteView(AdminUserRequiredMixin, DeleteView):
    model = DataTemplet
    template_name = 'devm/delete_confirm.html'
    success_url = reverse_lazy('devm:data-templet-list')


class DataTptModalListView(AdminUserRequiredMixin, ListView):
    paginate_by = settings.CONFIG.DISPLAY_PER_PAGE
    model = DataTemplet
    context_object_name = 'device_modal_list'
    template_name = 'devm/data_templet_modal_list.html'

    def get_context_data(self, **kwargs):
        devices = DataTemplet.objects.all()
        devices_id = self.request.GET.get('device_id', '')
        devices_id_list = [i for i in devices_id.split(',') if i.isdigit()]
        context = {
            'all_device': devices_id_list,
            'devices': devices
        }
        kwargs.update(context)
        return super(DataTptModalListView, self).get_context_data(**kwargs)

#
# def devm_index(request):
#     template_name = 'devm/index.html'
#     #access_list = Access_Log.objects.all()
#     #top = sort_url_access_time(access_list)
#     #top = access_list
#     return render(request, template_name )
#
# class DevmListView(AdminUserRequiredMixin, ListView):
#     #model = Asset
#     template_name = 'devm/index.html'
#     print(template_name)
#
#     def get_queryset(self):
#         queryset = '' #super(DevmListView, self).get_queryset()
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super(DevmListView, self).get_context_data(**kwargs)
#         #weblist = WebSite.objects.all()
#         context.update({
#             'app': _('devm'),
#             'action': _('Devm List'),
#
#         })
#
#         kwargs.update(context)
#         return super(DevmListView, self).get_context_data(**kwargs)
        #return context