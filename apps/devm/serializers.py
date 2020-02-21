# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from rest_framework import viewsets, serializers, generics
from common.mixins import CustomFilterMixin
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from .models.datapoint import DataPoint
from .models.group import DeviceGroup
from .models.datatemplet import DataTemplet
from .models.device import Device
from .models.data import Data


class DeviceSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = '__all__'


    def get_field_names(self, declared_fields, info):
        fields = super(DeviceSerializer, self).get_field_names(declared_fields, info)
        fields.extend(['get_type_display'])
        return fields

    @staticmethod
    def get_is_online(obj):
        if obj.status == True:
            return True
        elif obj.status == False:
            return False
        else:
            return 'Unknown'


class DeviceGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    devices_amount = serializers.SerializerMethodField()
    devices = serializers.PrimaryKeyRelatedField(many=True, queryset=Device.objects.all())

    class Meta:
        model = DeviceGroup
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        #fields = ['id', 'name', 'comment', 'assets_amount', 'assets']

    @staticmethod
    def get_devices_amount(obj):
        return obj.devices.count()

class DataTpSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    data_point_amount = serializers.SerializerMethodField()

    class Meta:
        model = DataTemplet
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        #fields = ['id', 'name', 'comment', 'assets_amount', 'assets']

    @staticmethod
    def get_data_point_amount(obj):
        data_points = DataPoint.objects.all()
        return data_points.count()

class DataPointSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    # data_point_amount = serializers.SerializerMethodField()
    # data_point = serializers.PrimaryKeyRelatedField(many=True, queryset= DataPoint.objects.all())

    class Meta:
        model = DataPoint
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        #fields = ['id', 'name', 'comment', 'assets_amount', 'assets']


class DataSerializer(serializers.ModelSerializer):
    #date_start = serializers.DateTimeField

    class Meta:
        model = Data
        fields = '__all__'