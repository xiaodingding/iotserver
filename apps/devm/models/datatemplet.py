#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
import uuid
from django.db import models, IntegrityError
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

#from common.utils import signer, date_expired_default
from common.mixins import NoDeleteModelMixin


__all__ = ['DataTemplet']


class DataTemplet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    created_by = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

    def delete(self, using=None, keep_parents=False):
        if self.name != 'Default':
            return super(DataTemplet, self).delete()
        return True

    class Meta:
        ordering = ['name']

    @classmethod
    def initial(cls):
        default_templete = cls.objects.filter(name='Default')
        if not default_templete:
            templete = cls(name='Default', created_by='System', comment='Default Device group')
            templete.save()
        else:
            templete = default_templete[0]
        return templete

    @classmethod
    def generate_fake(cls, count=100):
        from random import seed, choice
        import forgery_py
        from users.models import User

        seed()
        for i in range(count):
            templete = cls(name=forgery_py.name.full_name(),
                        comment=forgery_py.lorem_ipsum.sentence(),
                        created_by=choice(User.objects.all()).username)
            try:
                templete.save()
            except IntegrityError:
                print('Error continue')
                continue
