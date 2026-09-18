"""Tests for the views of codethesaur.us"""
import logging
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from web.models import LookupData


def setUpModule():
    logging.disable(logging.CRITICAL)


def tearDownModule():
    logging.disable(logging.NOTSET)


class TestViews(TestCase):
    """TestCase for the views"""

    def test_index_view_GET(self):
        """test if index uses the correct templates"""
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_about_view_GET(self):
        """test if about uses the correct templates"""
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_index_view_not_GET(self):
        """test that index shouldn't allow POST/PUT/etc."""
        url = reverse('index')
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.put(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.head(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.options(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_about_view_not_GET(self):
        """test that about shouldn't allow POST/PUT/etc."""
        url = reverse('about')
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.put(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.head(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.options(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_invalid_page_gives_404_error(self):
        """ test if a page that doesn't exist returns a 404"""
        url = 'no_real_page'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'error404.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'concepts.html')

    def test_compare_concepts_view_both_valid_languages(self):
        """test if compare with 2 valid languages uses the correct templates"""
        url = reverse('index') + \
              '?concept=data_types&entry=python%3B3&entry=java%3B17'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_compare_concepts_view_both_invalid_languages(self):
        """test if compare with invalid languages uses the correct templates"""
        url = reverse('index') + '?concept=data_types&entry=cupcake&entry=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_one_valid_one_invalid_language(self):
        """
        test if compare with one invalid language uses the correct templates
        """
        url = reverse('index') + '?concept=data_types&entry=python&entry=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_invalid_concept(self):
        """test if compare with an invalid concept uses the correct templates"""
        url = reverse('index') + '?concept=boop&entry=python&entry=haskell'

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_single_concepts_view_valid_language(self):
        """test if reference with a valid language uses the correct templates"""
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_single_concepts_view_invalid_languages(self):
        """
        test if reference with an invalid language uses the correct templates
        """
        url = reverse('index') + '?concept=data_types&entry=cupcake'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_single_concepts_view_invalid_concept(self):
        """
        test if reference with an invalid concept uses the correct templates
        """
        url = reverse('index') + '?concept=boop&entry=python'

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_both_valid_friendly_languages(self):
        """test if compare with 2 valid languages uses the correct templates"""
        url = reverse('index') + \
              '?concept=data_types&entry=Python%3B3&entry=Java%3B17'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'errormisc.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_compare_concepts_view_both_invalid_friendly_languages(self):
        """test if compare with invalid languages uses the correct templates"""
        url = reverse('index') + '?concept=data_types&entry=Cupcake&entry=Donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_one_valid_one_invalid_friendly_language(self):
        """
        test if compare with one invalid language uses the correct templates
        """
        url = reverse('index') + '?concept=data_types&entry=Python&entry=donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

        url = reverse('index') + '?concept=data_types&entry=python&entry=Donut'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_compare_concepts_view_invalid_friendly_concept(self):
        """test if compare with an invalid concept uses the correct templates"""
        url = reverse('index') + '?concept=Boop&entry=python&entry=haskell'

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_single_concepts_view_valid_friendly_language(self):
        """test if reference with a valid language uses the correct templates"""
        url = reverse('index') + '?concept=Data Types&entry=python%3B3'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'errormisc.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_single_concepts_view_invalid_friendly_language(self):
        """
        test if reference with an invalid language uses the correct templates
        """
        url = reverse('index') + '?concept=data_types&entry=Cupcake'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'concepts.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'errormisc.html')

    def test_single_concepts_view_invalid_friendly_concept(self):
        """
        test if reference with an invalid concept uses the correct templates
        """
        url = reverse('index') + '?concept=Boop&entry=python'

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
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

    def test_api_not_found(self):
        """Test if an invalid API call returns a 404 error"""
        url = "http://localhost:8000/api/shared/config/config.env/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_single_concept_view_valid_language_version(self):
        """
        Test if the API response contains 'meta' and 'concepts' keys. And doesnt return error.
        """
        url = '/api/data_types/javascript/ECMAScript%202009/'
        
        # Send GET request to the URL
        response = self.client.get(url)

        # Check the response status
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Parse the response JSON
        response_data = response.json()

        # Assert that 'meta' and 'concepts' keys exist
        self.assertIn('meta', response_data)
        self.assertIn('concepts', response_data)

    def test_api_compare_valid(self):
        """Test api_compare with valid languages and versions"""
        url = reverse('api.compare', kwargs={
            'structure_key': 'data_types',
            'lang1': 'python',
            'version1': '3',
            'lang2': 'javascript',
            'version2': 'ECMAScript 2009'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.json()
        self.assertIn('meta', response_data)
        self.assertIn('concepts1', response_data)
        self.assertIn('concepts2', response_data)
        self.assertEqual(response_data['meta']['entry_1'], 'python')
        self.assertEqual(response_data['meta']['entry_2'], 'javascript')

    def test_concepts_view_valid_params(self):
        """Test concepts view with valid parameters that should return 200"""
        url = reverse('index') + '?concept=data_types&entry=python%3B3&entry=javascript%3BECMAScript%202023'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')

    def test_concepts_view_legacy_params(self):
        """Test concepts view with legacy lang/lang1/lang2 parameters"""
        url = reverse('compare') + '?concept=data_types&lang=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')

        url = reverse('compare') + '?concept=data_types&lang1=python%3B3&lang2=javascript%3BECMAScript%202023'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')

    def test_concepts_view_logging(self):
        """test if the concepts view correctly logs to the database"""
        # test single language
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        self.client.get(url)
        lookup = LookupData.objects.last()
        self.assertEqual(lookup.entry1, 'python')
        self.assertEqual(lookup.version1, '3')
        self.assertEqual(lookup.entry2, '')
        self.assertEqual(lookup.version2, '')
        self.assertEqual(lookup.structure, 'data_types')

        # test two languages
        url = reverse('index') + '?concept=data_types&entry=python%3B3&entry=javascript%3BECMAScript%202023'
        self.client.get(url)
        lookup = LookupData.objects.last()
        self.assertEqual(lookup.entry1, 'python')
        self.assertEqual(lookup.version1, '3')
        self.assertEqual(lookup.entry2, 'javascript')
        self.assertEqual(lookup.version2, 'ECMAScript 2023')
        self.assertEqual(lookup.structure, 'data_types')

    def test_api_logging(self):
        """test if the API calls correctly log to the database"""
        # test api_reference
        url = reverse('api.reference', kwargs={
            'structure_key': 'data_types',
            'lang': 'python',
            'version': '3'
        })
        self.client.get(url)
        lookup = LookupData.objects.last()
        self.assertEqual(lookup.entry1, 'python')
        self.assertEqual(lookup.version1, '3')
        self.assertEqual(lookup.entry2, '')
        self.assertEqual(lookup.version2, '')
        self.assertEqual(lookup.structure, 'data_types')

        # test api_compare
        url = reverse('api.compare', kwargs={
            'structure_key': 'data_types',
            'lang1': 'python',
            'version1': '3',
            'lang2': 'javascript',
            'version2': 'ECMAScript 2009'
        })
        self.client.get(url)
        lookup = LookupData.objects.last()
        self.assertEqual(lookup.entry1, 'python')
        self.assertEqual(lookup.version1, '3')
        self.assertEqual(lookup.entry2, 'javascript')
        self.assertEqual(lookup.version2, 'ECMAScript 2009')
        self.assertEqual(lookup.structure, 'data_types')


