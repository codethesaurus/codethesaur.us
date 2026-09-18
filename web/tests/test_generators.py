import json
from django.test import TestCase
from web.thesaurus_template_generators import generate_entry_template, generate_meta_template

class TestGenerators(TestCase):
    def test_generate_entry_template_valid(self):
        # Using python and data_types which should exist
        template_str = generate_entry_template('python', 'data_types')
        template = json.loads(template_str)
        
        self.assertEqual(template['meta']['language'], 'python')
        self.assertEqual(template['meta']['structure'], 'data_types')
        self.assertIn('concepts', template)
        # Should have some concepts
        self.assertTrue(len(template['concepts']) > 0)
        
        # Check a specific concept
        # We need to know at least one concept key from data_types
        # From meta_info.json/langs/data_types.json
        self.assertIn('boolean', template['concepts'])
        self.assertEqual(template['concepts']['boolean']['name'], 'Boolean')

    def test_generate_entry_template_with_version(self):
        template_str = generate_entry_template('python', 'data_types', version='3')
        template = json.loads(template_str)
        self.assertEqual(template['meta']['language_version'], '3')

    def test_generate_entry_template_invalid_structure(self):
        with self.assertRaises(ValueError):
            generate_entry_template('python', 'non_existent_structure')

    def test_generate_meta_template(self):
        template_str = generate_meta_template('new_structure', 'New Structure Name')
        template = json.loads(template_str)
        
        self.assertEqual(template['meta']['structure'], 'new_structure')
        self.assertEqual(template['meta']['structure_name'], 'New Structure Name')
        self.assertIn('categories', template)
        self.assertIn('First Category Name', template['categories'])
