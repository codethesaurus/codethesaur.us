from django.test import TestCase
from django.urls import resolve, reverse
from web.views import  index, about, compare, reference

# Test cases for web urls.

class IndexUrlTest(TestCase):

    def setUp(self):
        # Setup data that'll be use in each test.
        self.url = reverse('index')

    def test_root_url_can_be_accept_by_name(self):
        self.assertEqual(self.url, '/')

    def test_root_url_use_correct_view(self):
        self.assertEqual(resolve(self.url).func, index)

    
class AboutUrlTest(TestCase):

    def setUp(self):
        self.url = reverse('about')

    def test_root_url_can_be_accept_by_name(self):
        self.assertEqual(self.url, '/about/')

    def test_root_url_use_correct_view(self):
        self.assertEqual(resolve(self.url).func, about)


class CompareUrlTest(TestCase):

    def setUp(self):
        self.url = reverse('compare')

    def test_root_url_can_be_accept_by_name(self):
        self.assertEqual(self.url, '/compare/')

    def test_root_url_use_correct_view(self):
        self.assertEqual(resolve(self.url).func, compare)


class ReferenceUrlTest(TestCase):

    def setUp(self):
        self.url = reverse('reference')

    def test_root_url_can_be_accept_by_name(self):
        self.assertEqual(self.url, '/reference/')

    def test_root_url_use_correct_view(self):
        print(resolve(self.url))
        self.assertEqual(resolve(self.url).func, reference)