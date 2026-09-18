from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

class TestViewsExtra(TestCase):
    def test_concepts_invalid_structure(self):
        url = reverse('index') + '?concept=invalid_struct&entry=python%3B3'
        response = self.client.get(url)
        # Should show errors
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, "structure/concept isn", status_code=HTTPStatus.NOT_FOUND)

    def test_concepts_invalid_entry(self):
        url = reverse('index') + '?concept=data_types&entry=invalid_lang%3B1'
        response = self.client.get(url)
        # Should show errors
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, "entry", status_code=HTTPStatus.NOT_FOUND)
        self.assertContains(response, "isn", status_code=HTTPStatus.NOT_FOUND)
        self.assertContains(response, "valid", status_code=HTTPStatus.NOT_FOUND)

    def test_concepts_missing_version_file(self):
        # python exists, but let's try a version that doesn't have data_types.json
        # Note: If it doesn't exist at all, it might be a MissingEntryError if not in meta_info.json
        # but if it is in meta_info but file is missing, it's MissingStructureError.
        # Python 2 is likely in meta_info but might not have all files.
        url = reverse('index') + '?concept=queries&entry=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, "error_missing_structure.html")

    def test_single_entry_reference(self):
        url = reverse('index') + '?concept=data_types&entry=python%3B3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Reference for Python (version 3)')

    def test_api_reference_invalid(self):
        url = reverse('api.reference', kwargs={
            'structure_key': 'invalid_struct',
            'lang': 'python',
            'version': '3'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_api_compare_invalid_lang(self):
        url = reverse('api.compare', kwargs={
            'structure_key': 'data_types',
            'lang1': 'python',
            'version1': '3',
            'lang2': 'invalid_lang',
            'version2': '1'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_statistics_view(self):
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statistics.html')

    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about.html')
