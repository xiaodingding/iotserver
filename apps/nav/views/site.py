# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, SingleObjectMixin
from django.urls import reverse_lazy
from django.conf import settings

# from common.permissions import  IsOrgAdmin
# from orgs.utils import current_org
from nav.models import Site
from nav.form import SiteForm
from ..hands import AdminUserRequiredMixin, User, UserGroup


__all__ = [
    'SiteListView', 'SiteCreateView',
    'SiteUpdateView', 'SiteDetailView',
    'SiteDeleteView', 'SiteUserView',
]


class SiteListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'nav/site_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Site'),
            'action': _('Site List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteCreateView(AdminUserRequiredMixin, CreateView):
    model = Site
    form_class = SiteForm
    template_name = 'nav/site_create_update.html'
    success_url = reverse_lazy('nav:site-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Site'),
            'action': _('create site permission'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        site = form.save()
        site.created_by = self.request.user.username or 'System'
        site.save()
        return super(SiteCreateView, self).form_valid(form)


class SiteUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Site
    form_class = SiteForm
    template_name = 'nav/site_create_update.html'
    success_url = reverse_lazy("nav:site-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Site'),
            'action': _('Update site'),
            'api_action': "update",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteDetailView(AdminUserRequiredMixin, DetailView):
    model = Site
    form_class = SiteForm
    template_name = 'nav/site_detail.html'
    success_url = reverse_lazy("nav:site-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Site'),
            'action': _('Site detail'),

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SiteDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Site
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('nav:site-list')


class SiteUserView(AdminUserRequiredMixin,
                              SingleObjectMixin,
                              ListView):
    template_name = 'nav/nav_user.html'
    context_object_name = 'Site'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Site.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_users())
        return queryset

    def get_context_data(self, **kwargs):
        users = [str(i) for i in self.object.users.all().values_list('id', flat=True)]
        user_groups_remain = UserGroup.objects.exclude(
            Site=self.object)
        context = {
            'app': _('Site'),
            'action': _('Site user list'),
            'users': users,
            'user_groups_remain': user_groups_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
