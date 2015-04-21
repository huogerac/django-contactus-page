# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

import floppyforms.__future__ as forms
from floppyforms.widgets import TextInput, EmailInput, Textarea

from .models import Message, Topic


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['status', ]


class MessageTopicForm(forms.ModelForm):

    subject = forms.CharField(max_length=100, label=_('A subject'),
                              widget=TextInput(attrs={'placeholder': 'Contact'}))
    name = forms.CharField(max_length=30, label=_('Your full name'),
                           widget=TextInput(attrs={'placeholder': 'Name Surname'}))
    email = forms.EmailField(label=_('Email'),
                             widget=EmailInput(attrs={'placeholder': 'name@provider.com'}))

    class Meta:
        model = Message
        fields = ['message', ]
        widgets = {
            'message': Textarea(attrs={'placeholder': 'your contact reason...', 'rows': 4,}),
        }

    def __init__(self, *args, **kws):
        super(MessageTopicForm, self).__init__(*args, **kws)
        self.fields.keyOrder = ['subject', 'name', 'email', 'message']


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': Textarea(attrs={'placeholder': 'your message...', 'rows': 2,}),
        }
