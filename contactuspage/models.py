# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from urllib import urlencode

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from multisitesutils.models import SiteModel, Preferences

from .helpers import topic_key_generator

User = get_user_model()


class ContactUsPreferences(Preferences):
    email_to = models.EmailField(
        _('Email To (notification)'), max_length=254, default='', blank=True)


class Topic(SiteModel):
    TOPIC_STATUS = (('0', 'Open'),
                    ('1', 'In progress'),
                    ('2', 'Closed'))
    status = models.CharField(_('Status'), max_length=8,
                              choices=TOPIC_STATUS, default='0')
    subject = models.CharField(_('A subject'), max_length=100)
    author = models.ForeignKey(User, verbose_name=_('author'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    last_update = models.DateTimeField(_('last_update'), auto_now_add=True)
    key = models.CharField(max_length=60, editable=False)

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def __unicode__(self):
        return self.subject

    def save(self, *args, **kws):
        self.key = topic_key_generator(self.author.email)
        super(Topic, self).save(*args, **kws)

    def _build_url(self, base_url):
        params = {'author_id': self.author.pk, 'topic_id': self.pk,
                  'topic_key': self.key}
        return '{0}?{1}'.format(base_url, urlencode(params))

    @property
    def status_verbose(self):
        if self.status:
            return dict(Topic.TOPIC_STATUS)[self.status]
        return None

    @property
    def messages_url(self):
        base_url = reverse('contacts.topic.list')
        return self._build_url(base_url)

    @property
    def reply_url(self):
        base_url = reverse('contacts.topic.reply')
        return self._build_url(base_url)


class Message(SiteModel):
    topic = models.ForeignKey(Topic, verbose_name=_('topic'))
    author = models.ForeignKey(User, verbose_name=_('author'))
    message = models.TextField(_('message'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    read = models.BooleanField(_('read'), default=False)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __unicode__(self):
        return self.message

    @property
    def topic_url(self):
        return self.topic.messages_url
