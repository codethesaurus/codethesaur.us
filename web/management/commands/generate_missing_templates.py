from django.core.management import call_command
from django.core.management.base import BaseCommand

from web.models import ThesaurusEntry, ThesaurusMetaInfo

import os


class Command(BaseCommand):
    help = 'Generate missing language thesaurus files to be filled out'

    def handle(self, *args, **options):
        meta_info = ThesaurusMetaInfo()
        languages = meta_info.languages
        structures = meta_info.structures

        for language, language_name in languages.items():
            entry = ThesaurusEntry(language, language_name)
            if entry.language_dir is None:
                continue

            lang_root = os.path.realpath(entry.language_dir)
            for version in entry.versions():
                for structure in structures:
                    file_path = os.path.realpath(os.path.join(
                        entry.language_dir,
                        version,
                        structure + '.json'
                    ))
                    if not file_path.startswith(lang_root + os.sep):
                        continue
                    if not os.path.exists(file_path):
                        call_command(
                            'generate_template',
                            language,
                            structure,
                            language_version=version,
                        )