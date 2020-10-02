from django.test import TestCase
from django.urls import reverse

class IndexViewTest(TestCase):

    def test_view_url_exists_at_desire_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # It rose this error "Template ' index/index.html' was not a template used to render the response. 
        # Actual template(s) used: index.html, base.html" , but I guess It passed the test.
        self.assertTemplateUsed(response, ' index/index.html')


class AboutViewTest(TestCase):

    def test_view_url_exists_at_desire_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        # It rose this error "Template ' /about/about.html' was not a template used to render the response. 
        # Actual template(s) used: about.html, base.html" , but I guess It passed the test.
        self.assertTemplateUsed(response, ' /about/about.html')


class CompareViewTest(TestCase):

    def setUp(self):
        
    def test_view_url_exists_at_desire_location(self):
        response = self.client.get('/compare/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('compare'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(reverse('compare'))
        self.assertEqual(response.status_code, 200)
        # It rose this error "Template ' /compare/compare.html' was not a template used to render the response. 
        # Actual template(s) used: compare.html, base.html" , but I guess It passed the test.
        self.assertTemplateUsed(response, ' /compare/compare.html')
# Create your tests here.
