#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

#from common.utils import signer, date_expired_default
from common.mixins import NoDeleteModelMixin

from .datatemplet import DataTemplet

__all__ = ['DataPoint']


class DataPoint(models.Model):
    DATA_TYPE_CHOICES = (
        ('Numeric', _('Numeric')),
        ('ON/OFF', _('ON/OFF')),
    )

    DATA_MODE_CHOICES = (
        ('Only-Read', _('Only-Read')),
        ('Only-Write', _('Only-Write')),
        ('Read-And-Write', _('Read-And-Write')),
    )

    name = models.CharField(max_length=128,blank=True, verbose_name=_('Name'))                 #变量名
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    templet = models.ForeignKey(DataTemplet,blank=False,verbose_name=_('Templet Id'), on_delete=models.DO_NOTHING)
    slave_addr =  models.CharField(max_length=30, blank=True, default=1, verbose_name=_('Slave Id'))
    data_type = models.CharField(choices=DATA_TYPE_CHOICES, max_length=30, default='Numeric', verbose_name=_("Data Type"), blank=False)           #数据类型 （数值型、开关型）
    registaddr =  models.IntegerField(default=1, blank=True ,verbose_name=_("Register Addr"))         #寄存器地址
    data_mode =  models.CharField(choices=DATA_MODE_CHOICES, max_length=30, verbose_name=_('Data Mode'), default='Read-And-Write', blank=False)           #数据模式 （只读、只写、读写）
    data_len= models.IntegerField(default=1,blank=True, verbose_name=_("Data Len"))              #数据长度
    expre = models.CharField(max_length=120, blank=True,help_text="Expression example: *1.5 +2", verbose_name=_('Expression'))       #表达式（公式）
    isstore = models.BooleanField(default=False, verbose_name=_('IsStore'))             #是否存储
    data_uint = models.CharField(max_length=100, blank=False, default='Default', verbose_name=_('Data Uint'), help_text="Data Uint")       #单位
    uint_name = models.CharField(max_length=100, blank=False, default='Default', verbose_name=_('Uint Name'), help_text="Uint Name")       #单位名称
    data_key = models.CharField(max_length=100, blank=True, default='Key', verbose_name=_('Key'))               #字段名
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    created_by = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

    def delete(self, using=None, keep_parents=False):
        if self.name != 'Default':
            return super(DataPoint, self).delete()
        return True

    class Meta:
        ordering = ['name']

    @classmethod
    def initial(cls):
        default_data = cls.objects.filter(name='Default')
        if not default_data:
            data = cls(name='Default', created_by='System', comment='Default Device group')
            data.save()
        else:
            data = default_data[0]
        return data

    @classmethod
    def generate_fake(cls, count=100):
        from random import seed, choice
        import forgery_py
        from users.models import User

        seed()
        for i in range(count):
            data = cls(name=forgery_py.name.full_name(),
                        comment=forgery_py.lorem_ipsum.sentence(),
                        created_by=choice(User.objects.all()).username)
            try:
                data.save()
            except IntegrityError:
                print('Error continue')
                continue
