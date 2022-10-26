"""Tests for codethesaur.us urls"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from web.views import index, about, compare, reference, api_reference


class TestUrls(SimpleTestCase):
    """TestCase for the urls"""

    def test_index_url(self):
        """ensure the index url uses the index function"""
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_about_url(self):
        """ensure the about url uses the about function"""
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)

    def test_compare_url(self):
        """ensure the compare url uses the compare function"""
        url = reverse('compare')
        self.assertEqual(resolve(url).func, compare)

    def test_reference_url(self):
        """ensure the reference url uses the reference function"""
        url = reverse('reference')
        self.assertEqual(resolve(url).func, reference)

    def test_api_url(self):
        """ensure the api url uses the api function"""
        url = reverse('api', args=['classes', 'javascript', 'ECMAScript 2023'])
        self.assertEqual(resolve(url).func, api_reference)
