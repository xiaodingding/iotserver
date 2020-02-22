# ~*~ coding: utf-8 ~*~
#

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from mqtt.models.publisher import Server, Client

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
        help_texts = {
            'name': '* required'
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        help_texts = {
            'name': '* required'
        }
