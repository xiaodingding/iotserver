 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import uuid
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse

from .datatemplet import DataTemplet
from .device import Device



__all__ = ['Data']


class Data(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    device = models.ForeignKey(Device, blank=True, null=True, on_delete=models.SET_NULL)
    data_content = models.TextField(verbose_name=_('DataContent'))      #数据内容,用;进行分割不同的DataPoint
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))


    def __unicode__(self):
        return 'Data: %s' % self.data_content

    def __str__(self):
        return 'device_id: %s templet_id:%s data_content:%s date_created:%s' % (self.device_id, self.data_content,self.date_created)

    def delete(self, using=None, keep_parents=False):
        return super(Data, self).delete()



    class Meta:
        ordering = ['date_created']
        get_latest_by =['date_created']
