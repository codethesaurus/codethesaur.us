from django.test import SimpleTestCase
from django.urls import reverse, resolve
from web.views import index, about, compare, reference


class TestUrls(SimpleTestCase):
    def test_index_url(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)

    def test_about_url(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func, about)

    def test_compare_url(self):
        url = reverse("compare")
        self.assertEqual(resolve(url).func, compare)

    def test_reference_url(self):
        url = reverse("reference")
        self.assertEqual(resolve(url).func, reference)
