# ~*~ coding: utf-8 ~*~
#

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from mqtt.models.publisher import Server, Client, Auth, SecureConf, Data
from mqtt.models.connect import Topic

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        # fields = '__all__'
        fields = [
            'host', 'port', "secure", "protocol"
        ]
        help_texts = {
            'host': '* required',
            'port': '* required'
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'server', 'auth', "client_id", "keepalive",  "clean_session"
        ]
        help_texts = {
            'server': '* required',
            'auth': '* required'
        }

class AuthForm(forms.ModelForm):
    class Meta:
        model = Auth
        fields = [
            'user', 'password'
        ]
        help_texts = {
            'user': '* required',
            'password': '* required'
        }


class SecureConfForm(forms.ModelForm):
    class Meta:
        model = SecureConf
        fields = '__all__'
        help_texts = {
            # 'name': '* required'
        }

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['client', 'topic', 'qos', 'payload']
        help_texts = {
            'client': '* required',
            'topic': '* required',
            'qos': '* required',
            'payload': '* required',
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'wildcard', 'dollar']
        help_texts = {
            'name': '* required'
        }
