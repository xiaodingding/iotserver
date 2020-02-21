# ~*~ coding: utf-8 ~*~
import uuid

from django.core.cache import cache

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet

from common.mixins import CustomFilterMixin
from common.utils import get_logger

from . import serializers
from .models import Notice
from .serializers import NoticeSerializer
from .hands import IsSuperUser, IsValidUser, IsSuperUserOrAppUser


logger = get_logger(__name__)


class NoticeViewSet(CustomFilterMixin, BulkModelViewSet):
    queryset = Notice.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = serializers.NoticeSerializer

