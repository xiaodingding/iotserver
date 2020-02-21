# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, SingleObjectMixin
from django.urls import reverse_lazy
from django.conf import settings

# from common.permissions import  IsOrgAdmin
# from orgs.utils import current_org
from identify.models import Identify
from identify.form import IdentifyCreateForm, IdentifyForm
from ..hands import AdminUserRequiredMixin, User, UserGroup


__all__ = [
    'IdentifyListView', 'IdentifyCreateView',
    'IdentifyUpdateView', 'IdentifyDetailView',
    'IdentifyDeleteView', 'IdentifyUserView',
]


class IdentifyListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'identify/identify_list.html'
    def get_context_data(self, **kwargs):
        context = {
            'app': _('Identify'),
            'action': _('Identify List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class IdentifyCreateView(AdminUserRequiredMixin, CreateView):
    model = Identify
    form_class = IdentifyForm
    template_name = 'identify/identify_create_update.html'
    success_url = reverse_lazy('identify:identify-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Identify'),
            'action': _('create identify'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        identify = form.save()
        #device.device_ico = self.request.GET['']
        identify.created_by = self.request.user.username or 'System'
        identify.user = self.request.user
        identify.save()
        return super(IdentifyCreateView, self).form_valid(form)


class IdentifyUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Identify
    form_class = IdentifyForm
    template_name = 'identify/identify_create_update.html'
    success_url = reverse_lazy("identify:identify-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Identify'),
            'action': _('Update identify'),
            'api_action': "update",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class IdentifyDetailView(AdminUserRequiredMixin, DetailView):
    model = Identify
    form_class = IdentifyForm
    template_name = 'identify/identify_detail.html'
    success_url = reverse_lazy("identify:identify-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Identify'),
            'action': _('Identify detail'),

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class IdentifyDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Identify
    template_name = 'identify/delete_confirm.html'
    success_url = reverse_lazy('identify:identify-list')


class IdentifyUserView(AdminUserRequiredMixin,
                              SingleObjectMixin,
                              ListView):
    template_name = 'identify/identify_user.html'
    context_object_name = 'Identify'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Identify.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_users())
        return queryset

    def get_context_data(self, **kwargs):
        users = [str(i) for i in self.object.users.all().values_list('id', flat=True)]
        user_groups_remain = UserGroup.objects.exclude(
            Identify=self.object)
        context = {
            'app': _('Identify'),
            'action': _('Identify user list'),
            'users': users,
            'user_groups_remain': user_groups_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
