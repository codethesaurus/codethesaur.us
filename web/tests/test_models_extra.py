from django.test import TestCase
from web.models import ThesaurusEntry

class TestModelsExtra(TestCase):
    def setUp(self):
        self.entry = ThesaurusEntry("test_lang", "Test Language")
        self.entry.concepts = {
            "complete": {
                "code": "print(1)",
                "comment": "print one"
            },
            "code_only": {
                "code": "print(2)"
            },
            "comment_only": {
                "comment": "comment only"
            },
            "not_impl": {
                "not-implemented": True
            },
            "not_impl_with_comment": {
                "not-implemented": True,
                "comment": "not implemented yet"
            },
            "empty": {
                "code": ""
            }
        }

    def test_is_concept_complete(self):
        # complete: code + comment
        self.assertTrue(self.entry.is_concept_complete("complete"))
        # code_only: it has code, so it's "complete" per implementation (either code OR comment)
        self.assertTrue(self.entry.is_concept_complete("code_only"))
        # comment_only: it has comment, so it's "complete"
        self.assertTrue(self.entry.is_concept_complete("comment_only"))
        # empty: no code, no comment
        self.assertFalse(self.entry.is_concept_complete("empty"))
        # not_impl: explicitly marked as not-implemented, so it's "complete" knowledge
        self.assertTrue(self.entry.is_concept_complete("not_impl"))

    def test_has_any_implemented_in_category(self):
        # complete is implemented
        self.assertTrue(self.entry.has_any_implemented_in_category(["complete", "not_impl"]))
        # both not_impl and not_impl_with_comment are not-implemented
        self.assertFalse(self.entry.has_any_implemented_in_category(["not_impl", "not_impl_with_comment"]))

    def test_is_category_incomplete(self):
        # A category is incomplete if any of its implemented concepts is NOT complete (no code AND no comment)
        # "empty" has no code and no comment, so it's incomplete
        self.assertTrue(self.entry.is_category_incomplete(["complete", "empty"]))
        # "complete" and "not_impl" are both considered "complete" or don't contribute to incompleteness
        self.assertFalse(self.entry.is_category_incomplete(["complete", "not_impl"]))
        # Unknown concept also makes it incomplete
        self.assertTrue(self.entry.is_category_incomplete(["unknown_concept"]))
