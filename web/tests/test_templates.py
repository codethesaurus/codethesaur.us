import re
from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase


class TestTemplates(TestCase):
    """TestCase for templates"""

    def test_concept_card_no_code_or_comment(self):
        """an empty card shows the placeholder rather than an empty box"""
        rendered = render_to_string("concept_card.html", {
            "placeholder": "Not implemented in this language"
        })

        self.assertIn("ct-placeholder", rendered)
        self.assertIn("Not implemented in this language", rendered)
        self.assertNotIn("ct-code", rendered)
        self.assertNotIn("ct-comment", rendered)

    def test_concept_card_code_only(self):
        """code is wrapped in a .ct-code block and keeps the pygments `syntax` class"""
        rendered = render_to_string("concept_card.html", {
            "code": "<b>I am bold!</b>"
        })

        self.assertIn('class="syntax ct-code"', rendered)
        self.assertIn("<b>I am bold!</b>", rendered)
        self.assertNotIn("ct-comment", rendered)
        self.assertNotIn("ct-placeholder", rendered)

    def test_concept_card_comment_only(self):
        """a comment is rendered in a labelled note block"""
        rendered = render_to_string("concept_card.html", {
            "comment": "I am **bold** and *italic*, `let x = 1`."
        })

        self.assertIn("ct-comment", rendered)
        self.assertIn("ct-comment-label", rendered)
        self.assertIn("Note", rendered)
        self.assertIn("<strong>bold</strong>", rendered)
        self.assertIn("<em>italic</em>", rendered)
        self.assertIn("<code>let x = 1</code>", rendered)
        self.assertNotIn("ct-code", rendered)
        # no divider when there is no code above the comment
        self.assertNotIn("ct-comment-divider", rendered)

    def test_concept_card_code_and_comment_are_separated(self):
        """code and comment get distinct blocks with a divider between them"""
        rendered = render_to_string("concept_card.html", {
            "code": "<b>I am bold!</b>",
            "comment": "I am **bold** and *italic*, `let x = 1`."
        })

        self.assertIn('class="syntax ct-code"', rendered)
        self.assertIn("ct-comment-divider", rendered)
        self.assertIn("ct-comment", rendered)
        self.assertNotIn("ct-placeholder", rendered)
        # the divider sits between the code block and the note block
        self.assertLess(
            rendered.index("ct-code"),
            rendered.index("ct-comment-divider")
        )
        self.assertLess(
            rendered.index("ct-comment-divider"),
            rendered.index("ct-comment-label")
        )

    def test_concept_card_comment_multiline(self):
        """multi-line comments keep their line breaks"""
        rendered = render_to_string("concept_card.html", {
            "code": "",
            "comment": "I am a humble\nmulti-line comment in the\nform of a haiku"
        })

        self.assertIn(
            "I am a humble<br>multi-line comment in the<br>form of a haiku",
            rendered
        )

    def test_concept_card_comment_markdown_url(self):
        """markdown links in comments still render"""
        rendered = render_to_string("concept_card.html", {
            "comment": "I am a [url](http://url.com), I am not a url.py"
        })

        self.assertIn('<a href="http://url.com">url</a>', rendered)

    def test_concept_card_divider_is_hidden_from_assistive_tech(self):
        """the visual divider is decorative and must not be announced"""
        rendered = render_to_string("concept_card.html", {
            "code": "<b>code</b>",
            "comment": "a note"
        })

        divider = re.search(
            r'<div class="ct-comment-divider"[^>]*>', rendered
        )
        self.assertIsNotNone(divider)
        self.assertIn('aria-hidden="true"', divider.group(0))

    def test_concept_card_labels_the_language(self):
        """each entry card names its language so stacked mobile cards stay attributable"""
        rendered = render_to_string("concept_card.html", {
            "code": "<b>def f(): pass</b>",
            "language": {"name": "Python", "version": "3"}
        })

        self.assertIn("ct-cell-label", rendered)
        self.assertIn("Python", rendered)
        self.assertIn("3", rendered)

    def test_concept_card_language_label_is_optional(self):
        """without a language in context (e.g. the bare inclusion tag) no label renders"""
        rendered = render_to_string("concept_card.html", {
            "code": "<b>def f(): pass</b>"
        })

        self.assertNotIn("ct-cell-label", rendered)

    def test_concept_card_language_label_works_without_code(self):
        """a placeholder-only card is still labelled with its language"""
        rendered = render_to_string("concept_card.html", {
            "placeholder": "Not implemented in this language",
            "language": {"name": "Lua", "version": "5"}
        })

        self.assertIn("ct-cell-label", rendered)
        self.assertIn("Lua", rendered)


class TestConceptsTableCss(TestCase):
    """the compare layout swaps column headers for per-card labels on narrow screens"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.css = Path(settings.BASE_DIR) / "web" / "static" / "css" / "app.css"
        cls.text = cls.css.read_text(encoding="utf-8")

    def test_table_header_is_hidden_on_narrow_screens(self):
        """once cards stack, the column header row detaches and must be hidden"""
        narrow = re.search(
            r"@media\s*\(max-width:[^)]+\)\s*\{[^@]*?\.ct-table-header\s*\{[^}]*display:\s*none",
            self.text,
            re.DOTALL,
        )
        self.assertIsNotNone(narrow, "app.css must hide .ct-table-header below the stacking breakpoint")

    def test_cell_label_is_only_shown_on_narrow_screens(self):
        """the per-card label replaces the hidden header, so it must not double up on desktop"""
        self.assertRegex(
            self.text,
            r"\.ct-cell-label\s*\{[^}]*display:\s*none",
            "app.css must hide .ct-cell-label by default",
        )
        narrow = re.search(
            r"@media\s*\(max-width:[^)]+\)\s*\{[^@]*?\.ct-cell-label\s*\{[^}]*display:\s*block",
            self.text,
            re.DOTALL,
        )
        self.assertIsNotNone(narrow, "app.css must reveal .ct-cell-label below the stacking breakpoint")
