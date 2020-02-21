# coding:utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Identify
from common.utils import  get_logger


logger = get_logger(__file__)


class IdentifyForm(forms.ModelForm):
    class Meta:
        model = Identify
        fields = [
            'name', 'comment',"user"
        ]
        help_texts = {
            'name': '* required',
        }

class IdentifyCreateForm(forms.ModelForm):
    class Meta:
        model = Identify
        fields = [
            'name', 'comment',"user"
        ]
        help_texts = {
            'name': '* required'
        }

