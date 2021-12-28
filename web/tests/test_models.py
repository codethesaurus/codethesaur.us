"""test for the models"""
import json

from django.test import TestCase

from web.models import Language, MetaInfo, MetaStructure, StructureFileNotFound


class TestMetaStructures(TestCase):
    """TestCase for Language, MetaInfo and MetaStructure"""

    def setUp(self):
        """prepare sample data for the tests"""
        self.metainfo = MetaInfo()
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = json.load(meta_file)
        self.structures = meta_data["structures"]
        self.languages = meta_data["languages"]

        self.sample = dict()
        self.sample["structure_id"] = list(self.structures.keys())[0]
        self.sample["friendly_name"] = self.structures[self.sample["structure_id"]]
        self.sample["language_id"] = list(self.languages.keys())[0]
        self.sample["language_name"] = self.languages[self.sample["language_id"]]

        # generate a dummy language
        language_id = "abcdefg"
        language_name = "Alphabet language!"
        concepts = {
            "concept1": {"code": "abc"},
            "concept2": {"code": "abc", "comment": "My comment"},
            "concept3": {"not-implemented": "true"},
            "concept4": {"code": ["line1", "line2"]}
        }
        language = Language(language_id, language_name)

        # This is like the manual work of calling language.load_structure()
        language.concepts = concepts
        self.dummy_language = language

    def test_metainfo_structure(self):
        """test MetaInfo creation"""
        self.assertIsNotNone(self.metainfo)

    def test_metainfo_structure_friendly_name(self):
        """test MetaInfo#friendly_name"""
        test_key = self.metainfo.structure_friendly_name(
            self.sample["structure_id"])

        self.assertEqual(test_key, self.sample["friendly_name"])

    def test_metastructure_init(self):
        """test MetaStructure creation"""
        metastructure = MetaStructure(
            self.sample["structure_id"], self.sample["friendly_name"])

        self.assertIsNotNone(metastructure.categories)

    def test_language_init(self):
        """test Language creation"""
        language = Language(self.sample["language_id"], self.sample["language_name"])

        self.assertIsNotNone(language)
        self.assertIsNotNone(language.key)
        self.assertEqual(language.concepts, dict())

    def test_language_bad_key_and_lang_exists(self):
        """test Language behaviour with bad language key"""
        language = self.dummy_language

        self.assertEqual(bool(language), False)
        self.assertRaises(StructureFileNotFound,
                          language.load_concepts,  "notastructure")


    # Commented out as the function *technically* works, but it can't
    # ensure that the sample concept and language actually exist. So
    # if someone can think of a better solution, I'm here for it!

    # def test_language_has_key_and_lang_exists(self):
    #     """test Language behaviour with good key and existing structure"""
    #     language = Language(self.sample["language_id"])
    #
    #     self.assertEqual(language.has_key(), True)
    #     self.assertEqual(language.lang_exists(), True)
    #
    #     language.load_structure(self.sample["structure_id"])
    #     self.assertEqual(language.has_key(), True)

    def test_language_get_concept(self):
        """test concept retrieval of a Language"""
        language = self.dummy_language
        # Test unknown concept
        self.assertEqual(language.concept("12345"), dict({
            "code": "",
            "comment": ""
        }))
        # Test known concept
        self.assertEqual(language.concept("concept1"), dict({"code": "abc"}))
        self.assertEqual(language.concept("concept2"), dict(
            {"code": "abc", "comment": "My comment"}))
        self.assertEqual(language.concept("concept3"), dict(
            {"code": "", "comment": "", "not-implemented": True}))
        self.assertEqual(language.concept("concept4"),
                          dict({"code": ["line1", "line2"]}))

    def test_language_concept_unknown(self):
        """test unknown concepts"""

        language = self.dummy_language

        # Test unknown concept
        self.assertEqual(language.concept_unknown("12345"), True)
        # Test known concept
        self.assertEqual(language.concept_unknown("concept1"), False)
        self.assertEqual(language.concept_unknown("concept2"), False)
        self.assertEqual(language.concept_unknown("concept3"), False)
        self.assertEqual(language.concept_unknown("concept4"), False)

    def test_language_concept_implemented(self):
        """test Language#concept_implemented"""
        language = self.dummy_language

        # Test unknown concept
        self.assertEqual(language.concept_implemented(
            "12345"), True)  # Shouldn't this be false

        # Test known concept
        self.assertEqual(language.concept_implemented("concept1"), True)
        self.assertEqual(language.concept_implemented("concept2"), True)
        self.assertEqual(language.concept_implemented("concept3"), False)
        self.assertEqual(language.concept_implemented("concept4"), True)

    def test_language_get_concept_code(self):
        """test Language#get_concept_code"""
        language = self.dummy_language

        # Test unknown concept
        self.assertEqual(language.concept_code("12345"), "")

        # Test known concept
        self.assertEqual(language.concept_code("concept1"), "abc")
        self.assertEqual(language.concept_code("concept2"), "abc")
        self.assertEqual(language.concept_code("concept3"), "")
        self.assertEqual(language.concept_code("concept4"), "line1\nline2")

    def test_language_get_concept_comment(self):
        """test Language#get_concept_comment"""
        language = self.dummy_language

        # Test unknown concept
        self.assertEqual(language.concept_comment("12345"), "")

        # Test known concept
        self.assertEqual(language.concept_comment("concept1"), "")
        self.assertEqual(language.concept_comment("concept2"), "My comment")
        self.assertEqual(language.concept_comment("concept3"), "")
        self.assertEqual(language.concept_comment("concept4"), "")
