# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django import template

from ..models import Topic

register = template.Library()


@register.inclusion_tag('contactuspage/show_contacts_messages_tag.html')
def show_contacts_messages_tag(is_contactus_admin=False, *args, **kwargs):
    """
    Show the icon + the number of unread messages
    """
    unread_messages = Topic.site_objects.all().exclude(status='2')
    return {'is_contactus_admin': is_contactus_admin,
            'messages': unread_messages.count()}
