# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import


def is_site_owner(request):
    if request.user.is_authenticated():
        if request.user.is_staff or request.user.is_superuser:
            return True
    return False


def send_email(message_type, data, subject, email_to, reply_to):
    print "--> [{0}] using {1}, sending {2} to: {3} (reply_to {4}".format(
        message_type,
        data,
        subject,
        email_to,
        reply_to)
