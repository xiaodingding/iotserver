# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, SingleObjectMixin
from django.urls import reverse_lazy
from django.conf import settings

# from common.permissions import  IsOrgAdmin
# from orgs.utils import current_org
from nav.models import SiteInfo
from nav.form import SiteInfoForm
from ..hands import AdminUserRequiredMixin, User, UserGroup


__all__ = [
    'SiteInfoListView', 'SiteInfoCreateView',
    'SiteInfoUpdateView', 'SiteInfoDetailView',
    'SiteInfoDeleteView', 'SiteInfoUserView',
]


class SiteInfoListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'nav/siteinfo_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('SiteInfo'),
            'action': _('SiteInfo List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteInfoCreateView(AdminUserRequiredMixin, CreateView):
    model = SiteInfo
    form_class = SiteInfoForm
    template_name = 'nav/siteinfo_create_update.html'
    success_url = reverse_lazy('nav:siteinfo-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('SiteInfo'),
            'action': _('create siteinfo permission'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        siteinfo = form.save()
        siteinfo.created_by = self.request.user.username or 'System'
        siteinfo.save()
        return super(SiteInfoCreateView, self).form_valid(form)


class SiteInfoUpdateView(AdminUserRequiredMixin, UpdateView):
    model = SiteInfo
    form_class = SiteInfoForm
    template_name = 'nav/siteinfo_create_update.html'
    success_url = reverse_lazy("nav:siteinfo-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('SiteInfo'),
            'action': _('Update siteinfo'),
            'api_action': "update",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteInfoDetailView(AdminUserRequiredMixin, DetailView):
    model = SiteInfo
    form_class = SiteInfoForm
    template_name = 'nav/siteinfo_detail.html'
    success_url = reverse_lazy("nav:siteinfo-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('SiteInfo'),
            'action': _('SiteInfo detail'),

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteInfoDeleteView(AdminUserRequiredMixin, DeleteView):
    model = SiteInfo
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('nav:siteinfo-list')


class SiteInfoUserView(AdminUserRequiredMixin,
                              SingleObjectMixin,
                              ListView):
    template_name = 'nav/nav_user.html'
    context_object_name = 'SiteInfo'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SiteInfo.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_users())
        return queryset

    def get_context_data(self, **kwargs):
        users = [str(i) for i in self.object.users.all().values_list('id', flat=True)]
        user_groups_remain = UserGroup.objects.exclude(
            SiteInfo=self.object)
        context = {
            'app': _('SiteInfo'),
            'action': _('SiteInfo user list'),
            'users': users,
            'user_groups_remain': user_groups_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
