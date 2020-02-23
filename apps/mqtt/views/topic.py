# -*- coding: utf-8 -*-
#

from django.views.generic import ListView, UpdateView, DeleteView, \
    DetailView, CreateView, TemplateView
from django.views.generic.edit import SingleObjectMixin
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy, reverse

from users.utils import AdminUserRequiredMixin
# from common.mixins import DatetimeSearchMixin
from mqtt.models.connect import Topic
from mqtt.forms import TopicForm



__all__ = [
    "TopicListView", "TopicUpdateView", "TopicDetailView",
    "TopicDeleteView"
]


class TopicListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'mqtt/topic_list.html'

    def get_context_topic(self, **kwargs):
        context = super(TopicListView, self).get_context_topic(**kwargs)
        context.update({
            'app': _('Topic'),
            'action': _('Topic list'),

        })
        return context


class TopicCreateView(AdminUserRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'mqtt/topic_create_update.html'
    success_url = reverse_lazy('mqtt:topic-list')
    # permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def get_context_topic(self, **kwargs):
        context = {
            'app': _('Topic'),
            'action': _('create topic'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_topic(**kwargs)

    def form_valid(self, form):
        topic = form.save()
        topic.created_by = self.request.user.username or 'System'
        topic.save()
        return super(TopicCreateView, self).form_valid(form)


class TopicUpdateView(AdminUserRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'mqtt/topic_create_update.html'
    success_url = reverse_lazy('mqtt:topic-list')

    def get_context_topic(self, **kwargs):
        context = super(TopicUpdateView, self).get_context_topic(**kwargs)
        context.update({'app': _('Topic'), 'action': _('Update topic')})
        return context


class TopicDetailView(AdminUserRequiredMixin, DetailView):
    model = Topic
    template_name = 'mqtt/topic_detail.html'
    context_object_name = 'topic'

    def get_context_topic(self, **kwargs):
        context = super(TopicDetailView, self).get_context_topic(**kwargs)
        context.update({
            'app': _('Topic'),
            'action': _('Topic detail')
        })
        return context


class TopicDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Topic
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('topic:topic-list')

