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
        
        for language in languages:
            versions = ThesaurusEntry(language, languages[language]).versions()
            for version in versions:
                for structure in structures:
                    file_path = os.path.join(
                        'web',
                        'thesauruses',
                        language,
                        version,
                        structure + '.json'
                    )
                    if not os.path.exists(file_path):
                        call_command(
                            'generate_template',
                            language,
                            structure,
                            language_version=version,
                        )