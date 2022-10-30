import unicodedata
from django.core.management.base import BaseCommand

from web.thesaurus_template_generators import generate_language_template
from web.models import MetaInfo
from packaging.version import parse as parse_version

import os


class Command(BaseCommand):
    help = 'Generate language thesaurus files to be filled out'

    def add_arguments(self, parser):
        structures = list(MetaInfo().structures.keys())

        parser.add_argument('language', help="Id of the programming language")
        parser.add_argument(
                'structures',
                nargs='+',
                help="Id(s) of the structure(s)",
                choices=structures
                )
        parser.add_argument('--language-version', required=True)

    def handle(self, *args, **options):
        for structure in options['structures']:
            self.generate_file(options['language'], structure, options['language_version'])

    def generate_file(self, language, structure, language_version):
        try:
            template = generate_language_template(
                language,
                structure,
                language_version,
            )
        except ValueError:
            self.stdout.write(
                    f'The structure "{structure}" is not implemented yet. You can visit https://docs.codethesaur.us/thesaurus/ to learn how to add one.'
            )

        version = parse_version(language_version)
        major_version = getattr(version, 'major', version.base_version)

        language_dir_path = os.path.join(
            'web',
            'thesauruses',
            language
        )

        if not os.path.exists(language_dir_path):
            warn = self.style.WARNING
            self.stdout.write(
                f'{warn("NOTE:")} The language "{language}" '\
                 'did not exist yet, make sure to add it in '\
                f'"{warn("web/thesauruses/meta_info.json")}" and adjust '\
                 '"language_name" in the "meta" section or it will not be '\
                 'picked up!\n\n'
            )
            os.mkdir(language_dir_path)

        template_file_directory = os.path.join(
            language_dir_path,
            f'{major_version}'
        )

        if not os.path.exists(template_file_directory):
            os.mkdir(template_file_directory)

        template_file_path = os.path.join(
            template_file_directory,
            f"{structure}.json"
        )

        if os.path.exists(template_file_path):
            self.stderr.write(
                f'"{template_file_path}" already exists, but you can still make your edits there.')
        else:
            with open(template_file_path, 'w') as file:
                file.write(template)
            self.stdout.write(
                 'Created template file '\
                f'"{self.style.SUCCESS(template_file_path)}" which you can '\
                 'now edit.'
            )