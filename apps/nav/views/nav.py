# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, SingleObjectMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import reverse, redirect

# from common.permissions import  IsOrgAdmin
# from orgs.utils import current_org
from nav.models import Category, Site, SiteInfo
from nav.form import SiteForm
from ..hands import AdminUserRequiredMixin, User, UserGroup
from common.utils import get_logger, get_object_or_none, is_uuid



__all__ = [
    'NavIndexView', 'NavAboutView',
]

logger = get_logger(__name__)

def get_site_info(sites):
    site_tag = ""
    row_flag = 0
    if len(sites) > 0:
        for site in sites:
            if(row_flag == 0):
                site_tag += '<div class="row">'
                row_flag = row_flag + 1
            # print(site.get('name'))
            site_tag += '<div class="col-sm-3">' +\
            '<div class="xe-widget xe-conversations box2 label-info" onclick="window.open(\'' + site.site_url +\
            '\', \'_blank\')" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="' + site.site_url + '">' +\
            '<div class="xe-comment-entry"><a class="xe-user-img"><img data-src="' + site.image_url.url + '" class="lozad img-circle" src="' + site.image_url.url +\
            '" data-loaded="true" width="40">' + '</a><div class="xe-comment"><a href="#" class="xe-user-name overflowClip_1"><strong>' +\
            site.name + '</strong></a><p class="overflowClip_2">' + site.desc + '</p></div></div></div></div>'
            if(row_flag >= 3):
                site_tag += '</div>'
                row_flag = 0
        if(row_flag > 0):
            site_tag += '</div>'
        row_flag = 0
    site_tag += '<br>'
    return site_tag

def get_site_tag(major_categorys):
    site_tag = ""
    if len(major_categorys) > 0:
        for major in major_categorys:
            minor = major.child.all()
            if len(minor) > 0:
                site_tag += get_site_tag(minor)
            else:
                site_tag += '<h4 class="text-gray"><i class="linecons-tag" style="margin-right: 7px;" id="' +\
                major.name + '"></i>' + major.name + '</h4>'

                sites = Site.objects.filter(smallcategory= major).all()
                site_tag += get_site_info(sites)
    return site_tag

def get_major_tag(major_categorys):
    nav_tag = ""
    if len(major_categorys) > 0:
        for major in major_categorys:
            minor = major.child.all()
            if len(minor) > 0:
                nav_tag += '<li> <a> <i class="' + major.icon_class + '"></i>' +\
                    ' <span class="title">' + major.name + '</span></a>'
                nav_tag += '<ul>' + get_major_tag(minor) + '</ul>'
            else:
                nav_tag += '<li> <a href="#' + major.name + '" class="smooth"> <i class="' + major.icon_class + '"></i>' +\
                    ' <span class="title">' + major.name + '</span></a>'
        nav_tag += '</li>'
    else:
        nav_tag = '<li>抱歉，列表为空</li>'
    return nav_tag


class NavIndexView(TemplateView):
    template_name = 'nav/nav_index.html'

    def get(self, request, *args, **kwargs):
        return super(NavIndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.debug("current user:{}".format(self.request.user.username) )

        major = Category.objects.filter(parent=None)
        major_tag = get_major_tag(major)
        site_tag = get_site_tag(major)
        site_info = SiteInfo.objects.first()
        context = {
            'major': major,
            'major_tag': major_tag,
            'site_tag': site_tag,
            'site_info': site_info
        }
        kwargs.update(context)
        return super(NavIndexView, self).get_context_data(**kwargs)



class NavAboutView(TemplateView):
    template_name = 'nav/nav_about.html'

    def get_context_data(self, **kwargs):
        major = Category.objects.filter(parent=None)
        major_tag = get_major_tag(major)
        site_tag = get_site_tag(major)
        site_info = SiteInfo.objects.first()
        context = {
            'major': major,
            'major_tag': major_tag,
            'site_tag': site_tag,
            'site_info': site_info
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

