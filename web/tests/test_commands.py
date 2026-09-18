import os
import shutil
from io import StringIO
from unittest.mock import Mock, patch
from django.core.management import call_command
from django.test import TestCase

class TestCommands(TestCase):
    def test_validatemetainfofile_command(self):
        out = StringIO()
        call_command('validatemetainfofile', stdout=out)
        self.assertIn('No errors found in meta_info.json.', out.getvalue())

    def test_validatelanginfofiles_command(self):
        out = StringIO()
        # This might take a while as it validates all files
        call_command('validatelanginfofiles', stdout=out)
        # It should at least finish without error and say something positive
        # Depending on the output of that command
        self.assertIn('no issues found', out.getvalue().lower())

    def test_generate_template_command(self):
        out = StringIO()
        test_lang = 'test_lang'
        test_version = '1.0'
        test_structure = 'data_types'
        
        # Ensure cleanup
        test_lang_dir = os.path.join('web', 'thesauruses', test_lang)
        if os.path.exists(test_lang_dir):
            shutil.rmtree(test_lang_dir)
            
        try:
            call_command(
                'generate_template', 
                test_lang, 
                test_structure, 
                language_version=test_version, 
                stdout=out
            )
            
            self.assertIn('Created template file', out.getvalue())
            
            # Verify file exists
            expected_file = os.path.join('web', 'thesauruses', test_lang, '1', f'{test_structure}.json')
            self.assertTrue(os.path.exists(expected_file))
            
        finally:
            # Cleanup
            if os.path.exists(test_lang_dir):
                shutil.rmtree(test_lang_dir)

    def test_generate_missing_templates_command(self):
        # Expect the command to invoke generate_template via call_command
        # rather than shelling out with os.system.
        test_lang = 'test_lang'
        test_version = '1.0'
        test_structure = 'data_types'

        test_lang_dir = os.path.join('web', 'thesauruses', test_lang)
        if os.path.exists(test_lang_dir):
            shutil.rmtree(test_lang_dir)

        meta_mock = Mock()
        meta_mock.languages = {test_lang: 'Test Lang'}
        meta_mock.structures = {test_structure: 'Data Types'}

        entry_mock = Mock()
        entry_mock.versions.return_value = [test_version]

        try:
            with patch(
                'web.management.commands.generate_missing_templates.ThesaurusMetaInfo',
                return_value=meta_mock,
            ), patch(
                'web.management.commands.generate_missing_templates.ThesaurusEntry',
                return_value=entry_mock,
            ), patch(
                'web.management.commands.generate_missing_templates.call_command',
            ) as mock_call_command:
                call_command('generate_missing_templates', stdout=StringIO())

            mock_call_command.assert_called_once_with(
                'generate_template', test_lang, test_structure,
                language_version=test_version,
            )
        finally:
            if os.path.exists(test_lang_dir):
                shutil.rmtree(test_lang_dir)
