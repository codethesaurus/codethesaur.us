"""Tests for the views of codethesaur.us"""
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    """TestCase for the views"""

    def test_index_view_GET(self):
        """test if index uses the correct templates"""
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_about_view_GET(self):
        """test if about uses the correct templates"""
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_invalid_page_gives_404_error(self):
        url = 'no_real_page'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error404.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'concepts.html')

    def test_compare_concepts_view_both_valid_languages(self):
        """test if compare with 2 valid languages uses the correct templates"""
        url = reverse('index') + \
            '?concept=data_types&lang=python%3B3&lang=java%3B17'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_compare_concepts_view_invalid_languages(self):
        """test if compare with invalid languages uses the correct templates"""
        url = reverse('index') + '?concept=data_types&lang=cupcake&lang=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_one_valid_one_invalid_language(self):
        """
        test if compare with one invalid language uses the corret templates
        """
        url = reverse('index') + '?concept=data_types&lang=python&lang=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_invalid_concept(self):
        """test if compare with an invalid concept uses the corret tempates"""
        url = reverse('index') + '?concept=boop&lang=python&lang=haskell'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')


    def test_single_concepts_view_valid_language(self):
        """test if reference with a valid language uses the corret templates"""
        url = reverse('index') + '?concept=data_types&lang=python%3B3'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_single_concepts_view_invalid_languages(self):
        """
        test if reference with an invalid language uses the corret templates
        """
        url = reverse('index') + '?concept=data_types&lang=cupcake'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_single_concepts_view_invalid_concept(self):
        """
        test if reference with an invalid concept uses the corret tempates
        """
        url = reverse('index') + '?concept=boop&lang=python'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_robots_txt_get_allowed(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        lines = response.content.decode().splitlines()
        self.assertEqual(lines[0], "User-Agent: *")

    def test_robots_txt_post_disallowed(self):
        response = self.client.post("/robots.txt")

        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)
