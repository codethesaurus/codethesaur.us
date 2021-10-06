from django.apps import AppConfig


class MarkdownifyConfig(AppConfig):
    name = 'markdownify'

    def ready(self):
        import markdownify.checks
