# ~*~ coding: utf-8 ~*~

import json
import uuid

import time
from django.db import models
from django.core import signing
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask

from common.utils import  get_logger

__all__ = ["Category", "Site", "SiteInfo"]


logger = get_logger(__file__)

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name='标题', max_length=128)
    icon_class = models.CharField(verbose_name='图标标签', default='linecons-star', blank=True, max_length=128)
    order_by = models.IntegerField(verbose_name='顺序', default=0)
    is_deleted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=128, blank=True, null=True, default='')
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="child", on_delete=models.CASCADE)

    @property
    def short_id(self):
        return str(self.id).split('-')[-1]


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name
        ordering = ['order_by']


class Site(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name='站点名', max_length=20)
    order_by = models.IntegerField(verbose_name='顺序', default=0)
    desc = models.CharField(verbose_name='描述', max_length=512, blank=True)
    # verbose_name 外键在编辑文章界面展示的名字，on_delete=models.CASCADE 外键删除时被关联的表内的主键也强制删除
    smallcategory = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='导航菜单')
    is_deleted = models.BooleanField(default=False)
    # ImageField类型必须设置upload_to参数
    image_url = models.ImageField('图片', upload_to='images/SiteInfo/')
    site_url = models.URLField(verbose_name='地址', max_length=128, blank=True)
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    created_by = models.CharField(max_length=128, blank=True, null=True, default='')

    @property
    def short_id(self):
        return str(self.id).split('-')[-1]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '站点'
        verbose_name_plural = verbose_name
        ordering = ['order_by']

class SiteGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(verbose_name='站点名', max_length=20)
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    user = models.ManyToManyField('users.User', related_name='users', blank=True, verbose_name=_('User'))

    @property
    def short_id(self):
        return str(self.id).split('-')[-1]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = verbose_name

class SiteInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(verbose_name='站点名', max_length=20)
    logo_exp_url = models.ImageField('网站Logo导航展开图片', upload_to='images/SiteInfo/')
    logo_col_url = models.ImageField('网站Logo导航关闭图片', upload_to='images/SiteInfo/')
    favicon = models.ImageField('网站favicon图片', upload_to='images/SiteInfo/')
    short_desc = models.CharField(verbose_name='简短描述', max_length=512, blank=True)
    site_desc = models.TextField(verbose_name='站点描述', default='', blank=True)
    copyright = models.CharField(verbose_name='版权说明', max_length=512, blank=True)
    keywords = models.CharField(verbose_name='网站关键字', default='keyword', max_length=512, blank=True)
    site_url = models.CharField(verbose_name='网站网站', default='www.ddsiot.cn', max_length=512, blank=True)
    date_created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)

    @property
    def short_id(self):
        return str(self.id).split('-')[-1]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = verbose_name


