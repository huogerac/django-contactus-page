# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import time
from hashlib import sha1, sha224

from django.utils.text import slugify


def topic_key_generator(author_mail):
    """ generate a key for identify a topic """
    base_string = unicode(time.time()).encode('utf-8') + author_mail
    return sha224(base_string).hexdigest().encode('utf-8')


def username_generator(name, email, hash_limit=10):
    _hash = sha1(email).hexdigest()[:hash_limit].encode('utf-8')
    _name = slugify(name).replace('-', '').encode('utf-8')
    username_hash = '{0}_{1}'.format(_name, _hash)[:30]
    return username_hash


def is_contactus_admin(request):
    # TODO - make possible to customize this method by the user
    if request.user.is_authenticated():
        if request.user.is_staff or request.user.is_superuser:
            return True
    return False


def send_user_notification(message_type, data, subject, email_to, reply_to):
    # TODO - make possible to customize this method by the user
    print "--> [{0}] using {1}, sending {2} to: {3} (reply_to {4}".format(
        message_type,
        data,
        subject,
        email_to,
        reply_to)
