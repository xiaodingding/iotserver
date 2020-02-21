# ~*~ coding: utf-8 ~*~

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Notice



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = [
             'title', 'body',
        ]
        help_texts = {
            'title': '* required',
            'body': '* required',
        }

