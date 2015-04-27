from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from contactuspage.views import MessageTopicCreateView
from contactuspage.models import Topic


class HomePageTest(TestCase):

    def test_url_resolves_to_create_topic(self):
        found = resolve('/contactus/topic/create/')

        self.assertEqual(found.func.func_name, 'MessageTopicCreateView')

    def test_post_data_should_create_a_new_topic(self):
        REDIRECT_CODE = 302

        # Given the following request to the create contact
        request = HttpRequest()
        request.method = 'POST'
        request.POST['subject'] = 'New contact'
        request.POST['name'] = 'Visitor'
        request.POST['email'] = 'visitor@bla.com'
        request.POST['message'] = 'This is a test message'

        # When the MessageTopicCreateView receive the request
        response = MessageTopicCreateView.as_view()(request)

        # Then it should go to the success page and create a new topic
        self.assertEqual(response.status_code, REDIRECT_CODE)
        topic_list = Topic.objects.all()
        self.assertEqual(len(topic_list), 1)
