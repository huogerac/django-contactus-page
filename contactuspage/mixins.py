# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

from .models import Topic
from .helpers import is_contactus_admin

User = get_user_model()


def verify_credentials(request):
    properties = {'can_reply': False, 'author': None, 'topic': None}

    topic_id = request.GET.get('topic_id', '$')
    try:
        topic = Topic.objects.get(pk=topic_id)
    except (ValueError, Topic.DoesNotExist):
        topic = None

    properties['topic'] = topic

    if request.user.is_authenticated() and topic:
        if request.user.is_staff or request.user.is_superuser:
            properties['can_reply'] = True
            properties['author'] = request.user
            return properties

    author_id = request.GET.get('author_id', '$')
    topic_key = request.GET.get('topic_key', '$')

    try:
        author = User.objects.get(pk=author_id)
    except (ValueError, User.DoesNotExist):
        author = None

    if author and topic:
        if topic.key == topic_key and topic.author == author:
            properties['can_reply'] = True
            properties['author'] = author

    return properties


class CanReplyMixin(object):

    def get_context_data(self, **kwargs):
        context = super(CanReplyMixin, self).get_context_data(**kwargs)
        context['is_contactus_admin'] = is_contactus_admin(self.request)
        return context

    def dispatch(self, request, *args, **kws):
        credentials = verify_credentials(request)
        if not credentials['can_reply']:
            return HttpResponseForbidden('you can not reply this topic')

        self.author = credentials['author']
        self.topic = credentials['topic']
        return super(CanReplyMixin, self).dispatch(request, *args, **kws)


class ContactusAdminMixin(object):

    def dispatch(self, request, *args, **kws):
        if not is_contactus_admin(request):
            HttpResponseForbidden('you can not access this page')

        return super(ContactusAdminMixin, self).dispatch(
                    request, *args, **kws)
