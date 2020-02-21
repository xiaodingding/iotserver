# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core import serializers as ser
from rest_framework import viewsets, serializers, generics
from common.mixins import CustomFilterMixin
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from .models import Category, Site, SiteInfo
import urllib.parse


class CategorySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryAndSiteSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    sites= serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_sites(self, obj):
        sites_query_set = Site.objects.filter(smallcategory=obj).all()  # 拿到所有作者信息
        site_json = []
        for site_obj in sites_query_set:
            site_json.append({"id": site_obj.id, "name": site_obj.name, "image_url":site_obj.image_url.url, "site_url":site_obj.site_url})
        return  site_json


class CategoryTreeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    pId= serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    sites_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
        # fields = ('id', 'name', 'pId', 'children', 'icon_class')

    def get_pId(self, obj):
        if hasattr(obj, 'pId'):
            pId = obj.pId
        else:
            pId = 0
        return pId

    def get_children(self, obj):
        child_query_set = Category.objects.filter(parent=obj.id).all()
        child_json = []
        for child_obj in child_query_set:
            child_json.append({"id": child_obj.id, "name": child_obj.name, "icon_class":child_obj.icon_class, "order_by":child_obj.order_by})
        return child_json

    def get_sites_count(self, obj):
        return len(Site.objects.filter(smallcategory=obj).all())



class SiteSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Site
        list_serializer_class = BulkListSerializer
        fields = '__all__'

class SiteInfoSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = SiteInfo
        list_serializer_class = BulkListSerializer
        fields = '__all__'
