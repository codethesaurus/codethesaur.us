from django.template import Context, Template
from django.test import TestCase


class TestTemplateTags(TestCase):
    def test_concept_card_tag(self):
        template = Template(
            "{% load templatetags %}"
            "{% concept_card code comment placeholder %}"
        )
        context = Context({
            'code': 'print("Hello")',
            'comment': 'A simple print statement',
            'placeholder': ''
        })
        rendered = template.render(context)
        
        self.assertIn('print("Hello")', rendered)
        self.assertIn('A simple print statement', rendered)
        self.assertIn('ct-code', rendered)
        self.assertIn('ct-comment', rendered)

    def test_concept_card_tag_with_placeholder(self):
        """a card with no code and no comment renders the placeholder"""
        template = Template(
            "{% load templatetags %}"
            "{% concept_card code comment placeholder %}"
        )
        context = Context({
            'code': '',
            'comment': '',
            'placeholder': 'Not implemented in this language'
        })
        rendered = template.render(context)

        self.assertIn('ct-placeholder', rendered)
        self.assertIn('Not implemented in this language', rendered)
