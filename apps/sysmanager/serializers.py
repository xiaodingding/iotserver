# -*- coding: utf-8 -*-
#
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer

from common.utils import get_signer, validate_ssh_public_key
from common.mixins import BulkSerializerMixin
from .models import Notice

signer = get_signer()


class NoticeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

