from django.test import TestCase
from django.template import Context, Template

class TestTemplateTags(TestCase):
    def test_concept_card_tag(self):
        template = Template(
            "{% load templatetags %}"
            "{% concept_card code comment %}"
        )
        context = Context({
            'code': 'print("Hello")',
            'comment': 'A simple print statement'
        })
        rendered = template.render(context)
        
        self.assertIn('print("Hello")', rendered)
        self.assertIn('A simple print statement', rendered)
