# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (MessageTopicCreateView, ReplyView, MessageListView,
                    TopicListView, TopicCloseUpdateView)


urlpatterns = patterns('',  # noqa

    # Allow visitors send message to the site owner
    url(r'^topic/create/$',
        MessageTopicCreateView.as_view(),
        name='contacts.topic.create'),

    url(r'^topic/created/$',
        TemplateView.as_view(
        template_name="contactuspage/topic_created.html"),
        name='contacts.topic.created'),

    # List all open topics (contacus admin)
    url(r'^topic/list/$',
        TopicListView.as_view(),
        name='contacts.topic.full_list'),

    # List messages from a given topic
    url(r'^topic/message/list$',
        MessageListView.as_view(),
        name='contacts.topic.list'),

    # Reply message
    url(r'^topic/message/reply/$',
        ReplyView.as_view(),
        name='contacts.topic.reply'),

    # Close topic
    url(r'^topic/close/(?P<pk>\d+)/$',
        TopicCloseUpdateView.as_view(),
        name='contacts.topic.close'),

)
