# -*- coding: utf-8 -*-
#

from django.utils import timezone
from rest_framework import serializers
from .models.publisher import Server, Auth, SecureConf, Client, Data
from .models.connect import ClientId, Topic


class ServerSerializer(serializers.ModelSerializer):
    name= serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = Server

    def get_name(self, obj):
        return "mqtt://%s:%s" % (obj.host, obj.port)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['secure']:
            data['secure'] = ""
        return data

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user', 'created_by', 'date_created']
        model = Auth

class ClientSerializer(serializers.ModelSerializer):
    name= serializers.SerializerMethodField()
    server = ServerSerializer(many=False)
    auth = AuthSerializer(many=False)
    class Meta:
        fields = '__all__'
        model = Client
        depth = 1

    def get_name(self, obj):
        server = "mqtt://%s:%s" % (obj.server.host, obj.server.port)
        return server

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['client_id']:
            data['client_id'] = ""
        return data

class SecureConfSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        model = SecureConf

class ClientIdSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        model = ClientId

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Topic

class DataSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many =False)
    topic = TopicSerializer(many =False)
    class Meta:
        fields = '__all__'
        model = Data
        depth = 1

