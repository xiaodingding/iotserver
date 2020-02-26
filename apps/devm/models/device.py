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

from .group import DeviceGroup
from .datatemplet import DataTemplet
#from common.utils import signer, date_expired_default


__all__ = ['Device']


class Device(models.Model):
    TYPE_CHOICES = (
        ('Default', _('Default')),
        ('Lora Concentrator', _('Lora Concentrator')),
        ('NB-IOT', _('NB-IOT')),
        ('Lora Module', _('Lora Module')),
        ('NetworkIO', _('NetworkIO')),
        ('QR Code', _("QR Code")),
        ('Serial Server', _("Serial Server")),
    )

    PROTOCOL_CHOICES = (
        ('Default', _('Default')),
        ('Modbus RTU', _('Modbus RTU')),
        ('Modbus ASCII', _('Modbus ASCII')),
        ('Modbus TCP', _('Modbus TCP')),
        ('MQTT', _('MQTT')),
        ('JSON Active Upload', _("JSON Active Upload")),
        ('XML Active Upload', _("XML Active Upload")),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=20, unique=False, verbose_name=_('DeviceName'))
    groups = models.ManyToManyField(DeviceGroup, related_name='devices', blank=True, verbose_name=_('Device Group'))
    type = models.CharField(choices=TYPE_CHOICES, default='Default', max_length=100, blank=True, verbose_name=_('Type'))
    protocol = models.CharField(choices=PROTOCOL_CHOICES,default='JSON', max_length=100, blank=True, verbose_name=_('Protocol'))
    comment = models.TextField(max_length=256, blank=True, verbose_name=_('Comment'))
    datatemplet = models.ManyToManyField(DataTemplet, related_name='devices_templet', blank=True, verbose_name=_('Templet'))#数据模板
    created_by = models.CharField(max_length=30, default='', verbose_name=_('Created by'))
    status = models.BooleanField(default=0)  # 设备状态
    device_sn = models.CharField(max_length=128,  blank=False, default=uuid.uuid1(), help_text="MAC,ID,IMEI,Rister Code,deviceId ...", unique=False, verbose_name=_('Device SN'))
    device_pwd = models.CharField(max_length=128, blank=True, unique=False, default="123456", help_text="passwd,sn,sn,verifyCode", verbose_name=_('Device Password'))
    device_ico = models.CharField(max_length=1024, blank=True, unique=False, verbose_name=_('Device Ico'))
    device_lng = models.CharField(max_length=128, blank=True, unique=False, default="102.73,25.04", verbose_name=_('Device Longitude')) #地理坐标
    device_addr = models.CharField(max_length=128, unique=False, default="云南昆明", verbose_name=_('Device Address'))#安装地址

    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    def get_absolute_url(self):
        return reverse('devices:device-detail', args=(self.id,))


    @property
    def is_expired(self):
        # if self.date_expired and self.date_expired < timezone.now():
        #     return True
        # else:
        #     return False
        return False

    @property
    def is_valid(self):
        if self.is_active and not self.is_expired:
            return True
        return False


    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Default'

        if not self.device_ico:
            self.device_ico = ''

        super(Device, self).save(*args, **kwargs)
        # Add the current user to the default group.
        if not self.groups.count():
            group = DeviceGroup.initial()
            self.groups.add(group)




    def is_member_of(self, device_group):
        if device_group in self.groups.all():
            return True
        return False

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'type': self.get_type_display(),
            'groups': [group.name for group in self.groups.all()],
            'comment': self.comment,
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S') if self.date_expired is not None else None
        })


    def delete(self):
        self.is_deleted = True
        self.save()
        return

    class Meta:
        ordering = ['name']

    #: Use this method initial user
    @classmethod
    def initial(cls):
        user = cls(name='default',
                   type='Default',
                   status=0,
                   comment=_('default device'),
                   created_by=_('System'))
        user.save()
        user.groups.add(DeviceGroup.initial())

    def img_url(self):
        img_default = settings.STATIC_URL + "img/default.jpg"
        if self.device_ico:
            #if( (self.device_ico.find("jpg")>=0) and (self.device_ico.find("png")>=0)):
            return self.device_ico
            #else:
            #return img_default
        else:
            return img_default

    @classmethod
    def generate_fake(cls, count=100):
        from random import seed, choice
        import forgery_py
        from django.db import IntegrityError

        seed()
        for i in range(count):
            device = cls(name=forgery_py.name.full_name(),
                       type='',
                       comment=forgery_py.lorem_ipsum.sentence(),
                       created_by=choice(cls.objects.all()).username)
            try:
                device.save()
            except IntegrityError:
                print('Duplicate Error, continue ...')
                continue
            device.groups.add(choice(DeviceGroup.objects.all()))
            device.save()
