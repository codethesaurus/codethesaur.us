import os
from django.core.management.base import BaseCommand
from django.conf import settings

from pygments.formatters.html import HtmlFormatter

class Command(BaseCommand):
    help = 'Generate static CSS files from pygments styles'

    def handle(self, *args, **options):
        for style in settings.PYGMENTS_STYLES:
            self.generate_file(style)

    def generate_file(self, style):
        
        # we need to prepend the `syntax` class before every class selector in the stylesheet to make sure that the styles get applied
        # only to our code snippet and not any other DOM element that happens to have the same class name.
        css = HtmlFormatter.get_style_defs(HtmlFormatter(style=style), '.syntax')

        css_file_path = os.path.join(
            'web',
            'static',
            'css',
            f'pygments_{style}.css'
        )

        if os.path.exists(css_file_path):
            self.stdout.write(f'Overwriting stylesheet: {css_file_path} for style: {style}')
        
        # overwrite existing stylesheet so that it can be replaced with newer style versions or fixes
        with open(css_file_path, 'w') as file:
            file.write(css + '\n')
        self.stdout.write(f'Created css stylesheet: {css_file_path}')
