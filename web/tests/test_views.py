from django.test import TestCase
from django.urls import reverse

# Test cases for web views.

class IndexViewTest(TestCase):

    def test_view_url_exists_at_desire_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/index.html')
        self.assertTemplateUsed(response, 'base.html')


class AboutViewTest(TestCase):

    def test_view_url_exists_at_desire_location(self):
        response = self.client.get('/about/')

        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get('/about/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/about.html')
        self.assertTemplateUsed(response, 'base.html')

# add compare and reference testcase.
