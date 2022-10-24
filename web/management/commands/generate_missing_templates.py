from django.core.management.base import BaseCommand

from web.models import Language, MetaInfo

import os


class Command(BaseCommand):
    help = 'Generate missing language thesaurus files to be filled out'

    def handle(self, *args, **options):
        meta_info = MetaInfo()
        languages = meta_info.languages
        structures = meta_info.structures
        
        for language in languages:
            versions = Language(language, languages[language]).versions()
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
                        os.system(f'python manage.py generate_template "{language}" "{structure}" --language-version="{version}" --draft=True')