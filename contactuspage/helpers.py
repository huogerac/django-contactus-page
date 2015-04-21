# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import time
import importlib
from hashlib import sha1, sha224

from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def topic_key_generator(author_mail):
    """ generate a key for identify a topic """
    base_string = unicode(time.time()).encode('utf-8') + author_mail
    return sha224(base_string).hexdigest().encode('utf-8')


def username_generator(name, email, hash_limit=10):
    _hash = sha1(email).hexdigest()[:hash_limit].encode('utf-8')
    _name = slugify(name).replace('-', '').encode('utf-8')
    username_hash = '{0}_{1}'.format(_name, _hash)[:30]
    return username_hash


def get_is_contactus_admin(request):
    """
        Returns the user's defined method for who is contactus page admin
    """
    is_contactus_admin = getattr(settings,
                                 "CONTACTUS_PAGE_IS_ADMIN_METHOD", None)
    if not is_contactus_admin:
        raise ImproperlyConfigured(
            'The settings.CONTACTUS_PAGE_IS_ADMIN_METHOD parameter is not defined.')
    module_name, method_name = is_contactus_admin.rsplit('.', 1)
    module = importlib.import_module(module_name)
    method_result = getattr(module, method_name)(request)
    return method_result


def get_send_user_notification(message_type,
                               data,
                               subject,
                               email_to, reply_to):
    """
        Returns the user's defined method for sending notifications
    """
    send_user_notification = getattr(settings,
                                     "CONTACTUS_PAGE_SEND_USER_NOTIFICATION_METHOD", None)
    if not send_user_notification:
        raise ImproperlyConfigured(
            'The settings.CONTACTUS_PAGE_SEND_USER_NOTIFICATION_METHOD parameter is not defined.')
    module_name, method_name = send_user_notification.rsplit('.', 1)
    module = importlib.import_module(module_name)
    method_result = getattr(module, method_name)(message_type,
                                                 data,
                                                 subject,
                                                 email_to, reply_to)
    return method_result
