# coding:utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from nav.models import Site, Category, SiteInfo
from common.utils import  get_logger


logger = get_logger(__file__)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'icon_class', 'order_by', 'parent'
        ]
        help_texts = {
            'name': '* required',
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'icon_class', 'order_by', 'parent'
        ]
        widgets = {
            'parent': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select category')})

        }
        help_texts = {
            'name': '* required'
        }

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name', 'desc', 'smallcategory', 'order_by', 'image_url', 'site_url'
        ]
        help_texts = {
            'name': '* required'
        }

class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name', 'desc', 'smallcategory', 'order_by', 'image_url', 'site_url'
        ]
        widgets = {
            'smallcategory': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select site')})

        }
        help_texts = {
            'name': '* required'
        }


class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = [
            'name', 'logo_exp_url', 'logo_col_url', 'favicon', 'short_desc', 'site_desc', 'copyright', 'keywords', 'site_url'
        ]
        help_texts = {
            'name': '* required'
        }

class SiteInfoCreateForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = [
             'name', 'logo_exp_url', 'logo_col_url', 'favicon', 'short_desc', 'site_desc', 'copyright', 'keywords', 'site_url'
        ]
        widgets = {
            'smallcategory': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select site')})

        }
        help_texts = {
            'name': '* required'
        }

