# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core import serializers as ser
from rest_framework import viewsets, serializers, generics
from common.mixins import CustomFilterMixin
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from .models import Identify
import urllib.parse


class IdentifySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Identify
        fields = ['id', 'name', 'comment', 'date_created', 'created_by']
        # fields = '__all__'
