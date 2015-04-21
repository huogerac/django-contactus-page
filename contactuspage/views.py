# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db.models import Count
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from multisitesutils import preferences

from .models import Topic, Message
from .forms import (MessageTopicForm, ReplyForm, TopicForm)
from .helpers import username_generator, send_user_notification
from .mixins import ContactusAdminMixin, CanReplyMixin, is_contactus_admin

User = get_user_model()


class MessageTopicCreateView(CreateView):
    model = Message
    form_class = MessageTopicForm

    def get_success_url(self):
        return reverse("contacts.topic.created")

    def form_valid(self, form):
        instance = form.save(commit=False)
        data = form.cleaned_data
        username = username_generator(data['name'], data['email'])

        # TODO:
        # - Is it a good idea creating a new user for each message?
        # - how to relate the users created with the current site?

        author, _ = User.objects.get_or_create(
            email=data['email'],
            defaults={'username': username, 'first_name': data['name'],
                      'email': data['email']})

        topic = Topic.objects.create(subject=data['subject'], author=author)

        instance.topic = topic
        instance.author = author
        instance.save()

        contactus_settings = preferences.ContactUsPreferences
        send_email = contactus_settings and contactus_settings.email_to

        if send_email:
            current_site = Site.objects.get_current()
            subject = "%s - Notification" % current_site.domain
            data = {'domain': current_site.domain}

            send_user_notification("email_notify_owner",
                                   data, subject,
                                   [contactus_settings.email_to], None)

        return HttpResponseRedirect(self.get_success_url())


class TopicListView(ContactusAdminMixin, ListView):
    model = Topic
    queryset = Topic.site_objects.all().annotate(
        Count('message')).order_by('-last_update').exclude(status='2')


class MessageListView(CanReplyMixin, ListView):
    # Only site managers and topic's author can see messages here
    model = Message

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['reply_form'] = ReplyForm()
        return context

    def get_queryset(self, *args, **kws):
        topic = Topic.objects.get(pk=self.request.GET['topic_id'])
        qs = self.model.site_objects.all().filter(topic=topic)
        qs.update(read=True)
        return qs.order_by('-created')


class ReplyView(CanReplyMixin, CreateView):
    # Only site managers and topic's author can create messages here
    model = Message
    form_class = ReplyForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.topic = self.topic
        instance.author = self.author
        instance.save()
        contactus_admin = is_contactus_admin(self.request)

        if contactus_admin:
            topic = instance.topic
            topic.status = '1'
            topic.save()

        # TODO:
        # - add settings for the sender and Mail backend API
        contactus_settings = preferences.ContactUsPreferences
        send_email = contactus_settings and contactus_settings.email_to
        if send_email:
            current_site = contactus_settings.site
            subject = "%s - Notification" % current_site.domain

            if contactus_admin:
                # email the topic's author
                data = {'domain': current_site.domain,
                        'name': self.topic.author.first_name,
                        'reply_url': self.topic.messages_url}

                send_user_notification("email_notify_author",
                                       data, subject,
                                       [self.topic.author.email], None)

            else:
                # email the site owner
                data = {'domain': current_site.domain}
                send_user_notification("email_notify_owner",
                                       data, subject,
                                       [contactus_settings.email_to], None)

        return redirect(instance.topic_url)


class TopicCloseUpdateView(ContactusAdminMixin, UpdateView):
    model = Topic
    form_class = TopicForm

    def get_success_url(self):
        return reverse("contacts.topic.full_list")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.status = '2'
        instance.save()
        return HttpResponseRedirect(self.get_success_url())
