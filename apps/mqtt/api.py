# -*- coding: utf-8 -*-
#
from collections import OrderedDict
import logging
import os
import uuid

from rest_framework import viewsets, serializers
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_bulk import BulkModelViewSet

from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.files.storage import default_storage
from django.http import HttpResponseNotFound


from common.mixins import CustomFilterMixin
from common.utils import get_object_or_none
from .models.publisher import Auth, Client, SecureConf as Secure, Server, Data
from .models.connect import Topic
from .serializers import AuthSerializer, ClientSerializer, SecureConfSerializer, ServerSerializer, DataSerializer, TopicSerializer

logger = logging.getLogger(__file__)
class AuthViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Auth.objects.filter(is_deleted=False)
    serializer_class = AuthSerializer
    permission_classes = (IsAuthenticated,)

#viewsets.ModelViewSet 不能接受删除命令
#CustomFilterMixin ,BulkModelViewSet 自带删除命令

class ClientViewSet(CustomFilterMixin, BulkModelViewSet):
    # queryset = Client.objects.filter(is_deleted=False)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)

class ClientListAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, requset, *args, **kwargs):
        from django.core import serializers as ser
        instance = Client.objects.all()
        data = ser.serialize('json', instance)
        # return Response()
        return Response(data, content_type='application/json')

class SecureViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Secure.objects.filter(is_deleted=False)
    serializer_class = SecureConfSerializer
    permission_classes = (IsAuthenticated,)

class ServerViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Server.objects.filter(is_deleted=False)
    serializer_class = ServerSerializer
    permission_classes = (IsAuthenticated,)

class TopicViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Topic.objects.filter(is_deleted=False)
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated,)


class DataViewSet(CustomFilterMixin, BulkModelViewSet):
    # queryset = Client.objects.filter(is_deleted=False)
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    permission_classes = (IsAuthenticated,)
