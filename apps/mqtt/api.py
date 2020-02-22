# -*- coding: utf-8 -*-
#
from collections import OrderedDict
import logging
import os
import uuid

from rest_framework import viewsets, serializers
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.files.storage import default_storage
from django.http import HttpResponseNotFound

from common.utils import get_object_or_none
from .models.publisher import Auth, Client, Secure, Server
from .serializers import AuthSerializer, ClientSerializer, SecureSerializer, ServerSerializer


logger = logging.getLogger(__file__)


class AuthViewSet(viewsets.ModelViewSet):
    queryset = Auth.objects.filter(is_deleted=False)
    serializer_class = AuthSerializer
    permission_classes = (IsAuthenticated,)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_deleted=False)
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)


class SecureViewSet(viewsets.ModelViewSet):
    queryset = Secure.objects.filter(is_deleted=False)
    serializer_class = SecureSerializer
    permission_classes = (IsAuthenticated,)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.filter(is_deleted=False)
    serializer_class = ServerSerializer
    permission_classes = (IsAuthenticated,)
