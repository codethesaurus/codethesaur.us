"""Tests for the views of codethesaur.us"""
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    """TestCase for the views"""

    def test_index_view_get(self):
        """test if index uses the correct templates"""
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_about_view_get(self):
        """test if about uses the correct templates"""
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_compare_view_both_valid_languages(self):
        """test if compare with 2 valid languages uses the correct templates"""
        url = reverse('compare') + \
            '?concept=data_types&lang1=python&lang2=java'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compare.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_compare_view_invalid_languages(self):
        """test if compare with invalid languages uses the correct templates"""
        url = reverse('compare') + \
            '?concept=data_types&lang1=cupcake&lang2=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'compare.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_view_one_valid_one_invalid_language(self):
        """
        test if compare with one invalid language uses the corret templates
        """
        url = reverse('compare') + \
            '?concept=data_types&lang1=python&lang2=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'compare.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_view_empty_query_string(self):
        """
        test if compare with an empty query string uses the corret templates
        """
        url = reverse('compare')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'compare.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_view_invalid_concept(self):
        """test if compare with an invalid concept uses the corret tempates"""
        url = reverse('compare') + '?concept=boop'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'compare.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_reference_view_valid_language(self):
        """test if reference with a valid language uses the corret templates"""
        url = reverse('reference') + '?concept=data_types&lang=python'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reference.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_reference_view_invalid_languages(self):
        """
        test if reference with an invalid language uses the corret templates
        """
        url = reverse('reference') + '?concept=data_types&lang=cupcake'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'reference.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_reference_view_empty_query_string(self):
        """
        test if reference with an empty query string uses the corret templates
        """
        url = reverse('reference')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'reference.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_reference_view_invalid_concept(self):
        """
        test if reference with an invalid concept uses the corret tempates
        """
        url = reverse('reference') + '?concept=boop'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'reference.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')
