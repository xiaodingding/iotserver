# -*- coding: utf-8 -*-
#

from django.utils import timezone
from rest_framework import serializers

from .models.publisher import Server, Auth, SecureConf, Client, Data
from .models.connect import ClientId, Topic


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Server


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Auth


class SecureConfSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = SecureConf

class ClientSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = Client

class DataSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = Data

class ClientIdSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = ClientId

class TopicSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = Topic
