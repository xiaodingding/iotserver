#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import uuid
import time

from collections import OrderedDict

from django.conf import settings
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse



__all__ = ['Notice']



class Notice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255,
                             verbose_name=_('Notice Title'),
                             help_text=_('Enter notice title.'))
    body = models.TextField(blank=True, null=True,
                            verbose_name=_('Notice Description'),
                            help_text=_('Please offer notice details. Markdown enabled.'))
    created_by = models.CharField(max_length=64, default='', null=True, verbose_name=_('Create by'))
    date_created = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('sysmanager:notice_detail', [self.id])

    @property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notice"
        ordering = ['date_created']

        get_latest_by = ['date_created']
