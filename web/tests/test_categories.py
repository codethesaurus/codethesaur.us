"""Tests for category-based features"""
import json
import os
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from web.models import ThesaurusEntry, ThesaurusMetaInfo, MetaStructure

class TestCategories(TestCase):
    """TestCase for category-based logic and views"""

    def setUp(self):
        self.metainfo = ThesaurusMetaInfo()

    def test_metainfo_categories_loaded(self):
        """Test that categories are correctly loaded from meta_info.json"""
        self.assertIn('langs', self.metainfo.categories)
        self.assertIn('databases', self.metainfo.categories)
        self.assertEqual(self.metainfo.categories['langs'], 'Programming Languages')
        self.assertEqual(self.metainfo.categories['databases'], 'Databases')

    def test_metainfo_category_structures_loaded(self):
        """Test that category-specific structures are correctly loaded"""
        self.assertIn('langs', self.metainfo.category_structures)
        self.assertIn('databases', self.metainfo.category_structures)
        
        # Check some known structures
        self.assertIn('data_types', self.metainfo.category_structures['langs'])
        self.assertIn('queries', self.metainfo.category_structures['databases'])
        
        # Check that they are correctly partitioned (ideally)
        # Though the current implementation flattens them into self.structures for backward compatibility
        self.assertIn('data_types', self.metainfo.structures)
        self.assertIn('queries', self.metainfo.structures)

    def test_entry_category_location(self):
        """Test that ThesaurusEntry correctly finds its directory based on category"""
        # Test a language (langs category)
        python_entry = ThesaurusEntry('python', 'Python')
        self.assertIn(os.path.join('web', 'thesauruses', 'langs', 'python'), python_entry.language_dir)
        
        # Test a database (databases category)
        mysql_entry = ThesaurusEntry('mysql', 'MySQL')
        self.assertIn(os.path.join('web', 'thesauruses', 'databases', 'mysql'), mysql_entry.language_dir)

    def test_index_view_groups_by_category(self):
        """Test that index view groups entries by category in the context"""
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        languages_context = response.context['languages']
        # languages_context should be a list of dicts, each with 'key', 'label', 'entries', 'structures'
        
        categories_found = [c['key'] for c in languages_context]
        self.assertIn('langs', categories_found)
        self.assertIn('databases', categories_found)
        
        langs_cat = next(c for c in languages_context if c['key'] == 'langs')
        self.assertIn('python', langs_cat['entries'])
        self.assertIn('data_types', langs_cat['structures'])
        
        db_cat = next(c for c in languages_context if c['key'] == 'databases')
        self.assertIn('mysql', db_cat['entries'])
        self.assertIn('queries', db_cat['structures'])
        # Ensure 'data_types' is NOT in databases category if not defined there
        self.assertNotIn('data_types', db_cat['structures'])

    def test_compare_databases(self):
        """Test comparing two database entries"""
        # MySQL and PostgreSQL should both have 'queries'
        url = reverse('index') + '?concept=queries&entry=mysql%3B8&entry=postgresql%3B15'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'concepts.html')
        
        # Check that we have the database-specific titles/data
        self.assertContains(response, 'Comparing MySQL (version 8) and PostgreSQL (version 15)')
        self.assertContains(response, 'Queries')

    def test_invalid_structure_for_category_returns_error(self):
        """
        Test that requesting a structure not belonging to the entry's category 
        might result in a MissingStructureError (404).
        Actually, load_entries just tries to load the file. 
        If it's not there, it raises MissingStructureError.
        """
        # mysql does not have 'data_types.json' in its directory (I removed them in previous issue)
        url = reverse('index') + '?concept=data_types&entry=mysql%3B8'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'error_missing_structure.html')

    def test_api_reference_databases(self):
        """Test API reference for a database structure"""
        url = reverse('api.reference', kwargs={
            'structure_key': 'queries',
            'lang': 'mysql',
            'version': '8'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.content)
        self.assertEqual(data['meta']['language'], 'mysql')
        self.assertEqual(data['meta']['structure'], 'queries')

    def test_api_compare_databases(self):
        """Test API comparison for databases"""
        url = reverse('api.compare', kwargs={
            'structure_key': 'queries',
            'lang1': 'mysql',
            'version1': '8',
            'lang2': 'postgresql',
            'version2': '15'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = json.loads(response.content)
        self.assertEqual(data['meta']['entry_1'], 'mysql')
        self.assertEqual(data['meta']['entry_2'], 'postgresql')
        self.assertIn('concepts1', data)
        self.assertIn('concepts2', data)
