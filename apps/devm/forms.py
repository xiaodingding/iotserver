# coding:utf-8
from django import forms
from django.utils.translation import gettext_lazy as _

from .models.datapoint import DataPoint
from .models.group import DeviceGroup
from .models.datatemplet import DataTemplet
from .models.device import Device

from common.utils import validate_ssh_private_key, ssh_pubkey_gen, ssh_key_gen, get_logger


logger = get_logger(__file__)


class DeviceGroupForm(forms.ModelForm):
    # See AdminUserForm comment same it
    assets = forms.ModelMultipleChoiceField(
        queryset= Device.objects.all(),
        label=_('device'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': _('Select devices')})
        )

    # def __init__(self, *args, **kwargs):
    #     if kwargs.get('instance', None):
    #         initial = kwargs.get('initial', {})
    #         initial['devices'] = kwargs['instance'].assets.all()
    #     super(DeviceGroupForm, self).__init__(*args, **kwargs)

    def _save_m2m(self):
        super(DeviceGroupForm, self)._save_m2m()
        # assets = self.cleaned_data['devices']
        # self.instance.assets.clear()
        # self.instance.assets.add(*tuple(assets))

    class Meta:
        model = DeviceGroup
        fields = [
            "name", "comment",
        ]
        help_texts = {
            'name': '* required',
        }

class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'name', 'device_sn', 'device_pwd', 'device_ico', 'device_lng', 'device_addr', 'type', 'comment',
            'groups', 'status', 'is_active', 'datatemplet', 'protocol'
        ]
        widgets = {
            'groups': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select asset groups')}),

        }
        help_texts = {
            'name': '* required',
            'device_sn': '* required',
            # 'system_users': _('System user will be granted for user to login '
            #                   'assets (using ansible create automatic)'),
            # 'admin_user': _('Admin user should be exist on asset already, '
            #                 'And have sudo ALL permission'),
        }


class DataTptCreateForm(forms.ModelForm):
    class Meta:
        model = DataTemplet
        fields = [
            'name', 'comment'
        ]

        help_texts = {
            'name': '* required',
        }

    # def clean_admin_user(self):
    #     if not self.cleaned_data['admin_user']:
    #         raise forms.ValidationError(_('Select admin user'))
    #     return self.cleaned_data['admin_user']

class DataPointCreateForm(forms.ModelForm):
    class Meta:
        model = DataPoint
        fields = [
            'name', 'slave_addr', 'data_type', 'registaddr', 'data_mode', 'data_len',
            'expre', 'isstore', 'data_uint', 'data_key', 'comment', 'templet','uint_name'
        ]
        widgets = {
            'groups': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select asset groups')}),
            'admin_user': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select asset admin user')}),
        }
        help_texts = {
            'name': '* required',
            'data_type': '* required',
            'data_uint': '* required',
            'data_key': '* required',
        }

    # def clean_admin_user(self):
    #     if not self.cleaned_data['admin_user']:
    #         raise forms.ValidationError(_('Select admin user'))
    #     return self.cleaned_data['admin_user']
