# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, SingleObjectMixin
from django.urls import reverse_lazy
from django.conf import settings

# from common.permissions import  IsOrgAdmin
# from orgs.utils import current_org
from nav.models import Category
from nav.form import CategoryCreateForm, CategoryForm
from ..hands import AdminUserRequiredMixin, User, UserGroup


__all__ = [
    'CategoryListView', 'CategoryCreateView',
    'CategoryUpdateView', 'CategoryDetailView',
    'CategoryDeleteView', 'CategoryUserView',
]



class CategoryAndSitesListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'nav/category_site_tree.html'
    def get_context_data(self, **kwargs):
        context = {
            'app': _('Category'),
            'action': _('Category List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CategoryListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'nav/category_list.html'
    def get_context_data(self, **kwargs):
        context = {
            'app': _('Category'),
            'action': _('Category List'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CategoryCreateView(AdminUserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'nav/category_create_update.html'
    success_url = reverse_lazy('nav:category-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Category'),
            'action': _('create category'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        category = form.save()
        #device.device_ico = self.request.GET['']
        category.created_by = self.request.user.username or 'System'
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'nav/category_create_update.html'
    success_url = reverse_lazy("nav:category-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Category'),
            'action': _('Update category'),
            'api_action': "update",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CategoryDetailView(AdminUserRequiredMixin, DetailView):
    model = Category
    form_class = CategoryForm
    template_name = 'nav/category_detail.html'
    success_url = reverse_lazy("nav:category-list")

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Category'),
            'action': _('Category detail'),

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CategoryDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Category
    template_name = 'nav/delete_confirm.html'
    success_url = reverse_lazy('nav:category-list')


class CategoryUserView(AdminUserRequiredMixin,
                              SingleObjectMixin,
                              ListView):
    template_name = 'nav/nav_user.html'
    context_object_name = 'Category'
    paginate_by = settings.DISPLAY_PER_PAGE
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = list(self.object.get_all_users())
        return queryset

    def get_context_data(self, **kwargs):
        users = [str(i) for i in self.object.users.all().values_list('id', flat=True)]
        user_groups_remain = UserGroup.objects.exclude(
            Category=self.object)
        context = {
            'app': _('Category'),
            'action': _('Category user list'),
            'users': users,
            'user_groups_remain': user_groups_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
