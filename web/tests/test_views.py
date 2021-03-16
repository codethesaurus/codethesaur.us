from django.test import TestCase, Client
from django.urls import reverse
from web.views import index, about, compare, reference


class TestViews(TestCase):
    def test_index_view_GET(self):
        url = reverse("index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertTemplateUsed(response, "base.html")

    def test_about_view_GET(self):
        url = reverse("about")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertTemplateUsed(response, "base.html")

    def test_compare_view_GET(self):
        url = reverse("compare") + "?concept=data_types&lang1=python&lang2=java"
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "compare.html")
        self.assertTemplateUsed(response, "base.html")

    def test_reference_view_GET(self):
        url = reverse("reference") + "?concept=data_types&lang=python"
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reference.html")
        self.assertTemplateUsed(response, "base.html")
