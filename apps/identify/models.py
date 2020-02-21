# ~*~ coding: utf-8 ~*~

import json
import uuid

import time
from django.db import models
from django.core import signing
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from django.conf import settings

from common.utils import  get_logger

__all__ = ["Identify"]


logger = get_logger(__file__)

# Create your models here.
class Identify(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name='项目名称', max_length=128)
    secret = models.UUIDField(verbose_name='AccessKeySecret',
                              default=uuid.uuid4, editable=False)
    comment = models.TextField(blank=True, verbose_name=_("Comment"))
    is_deleted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=128, blank=True, null=True, default='')
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',
                             on_delete=models.CASCADE, related_name='access_keys')

    def get_id(self):
        return str(self.id)

    def get_secret(self):
        return str(self.secret)

    def get_full_value(self):
        return '{}:{}'.format(self.id, self.secret)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '用户授权'
        verbose_name_plural = verbose_name
        ordering = ['date_created']

