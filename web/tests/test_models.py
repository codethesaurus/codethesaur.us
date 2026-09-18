"""test for the models"""
import json
import os

from django.test import TestCase

from web.models import ThesaurusEntry, ThesaurusMetaInfo, MetaStructure


class TestMetaStructures(TestCase):
    """TestCase for ThesaurusEntry, ThesaurusMetaInfo and MetaStructure"""

    def setUp(self):
        """prepare sample data for the tests"""
        self.metainfo = ThesaurusMetaInfo()
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = json.load(meta_file)
        self.category_structures = meta_data["structures"]
        self.structures = {}
        for cat_structs in self.category_structures.values():
            self.structures.update(cat_structs)
        self.languages = meta_data["languages"]

        self.sample = dict()
        self.sample["structure_key"] = list(self.structures.keys())[0]
        self.sample["structure_name"] = self.structures[self.sample["structure_key"]]
        self.sample["language_key"] = list(self.languages.keys())[0]
        self.sample["language_name"] = self.languages[self.sample["language_key"]]

        # generate a dummy language
        language_key = "abcdefg"
        language_name = "Alphabet language!"
        concepts = {
            "concept1": {"code": "abc"},
            "concept2": {"code": "abc", "comment": "My comment"},
            "concept3": {"not-implemented": "true"},
            "concept4": {"code": ["line1", "line2"]}
        }
        language = ThesaurusEntry(language_key, language_name)

        # This is like the manual work of calling language.load_structure()
        language.concepts = concepts
        self.dummy_language = language

    def test_metainfo_structure(self):
        """test ThesaurusMetaInfo creation"""
        self.assertIsNotNone(self.metainfo)

    def test_metainfo_structure_name(self):
        """test ThesaurusMetaInfo#name"""
        test_key = self.metainfo.structure_name(
            self.sample["structure_key"])

        self.assertEqual(test_key, self.sample["structure_name"])

    def test_metastructure_init(self):
        """test MetaStructure creation"""
        metastructure = MetaStructure(
            self.sample["structure_key"], self.sample["structure_name"])

        self.assertIsNotNone(metastructure.categories)

    def test_language_init(self):
        """test ThesaurusEntry creation"""
        language = ThesaurusEntry(self.sample["language_key"], self.sample["language_name"])

        self.assertIsNotNone(language)
        self.assertIsNotNone(language.key)
        self.assertIsNone(language.concepts)

    def test_language_bad_key_and_lang_exists(self):
        """test ThesaurusEntry behaviour with bad language key"""
        language = self.dummy_language

        self.assertEqual(bool(language), False)
        self.assertRaises(FileNotFoundError,
                          language.load_concepts,  "notastructure", "notaversion")

    def test_malicious_language_key_cannot_escape_thesaurus_dir(self):
        """test that a user-controlled key cannot traverse out of the thesaurus dir"""
        for bad_key in ("..", "../..", "..\\..", "python/.."):
            with self.subTest(key=bad_key):
                entry = ThesaurusEntry(bad_key, "")
                self.assertIsNone(entry.language_dir)

    def test_language_dir_stays_within_thesaurus_root(self):
        """test that language_dir is confined to the thesaurus directory"""
        entry = ThesaurusEntry("python", "")
        thesaurus_root = os.path.realpath(
            os.path.join("web", "thesauruses"))
        self.assertIsNotNone(entry.language_dir)
        self.assertTrue(entry.language_dir.startswith(thesaurus_root + os.sep))

    def test_metastructure_rejects_path_traversal_key(self):
        """test that a malicious structure key never opens a file"""
        from unittest.mock import mock_open, patch

        with patch("builtins.open", mock_open()) as mocked_open:
            with self.assertRaises(FileNotFoundError):
                MetaStructure("../..", "")
        mocked_open.assert_not_called()

    def test_load_concepts_rejects_path_traversal_components(self):
        """test that a malicious structure/version never opens a file"""
        from unittest.mock import mock_open, patch

        entry = ThesaurusEntry("python", "")
        with patch("builtins.open", mock_open()) as mocked_open:
            with self.assertRaises(FileNotFoundError):
                entry.load_concepts("..", "3")
            with self.assertRaises(FileNotFoundError):
                entry.load_concepts("data_types", "../..")
        mocked_open.assert_not_called()


    # Commented out as the function *technically* works, but it can't
    # ensure that the sample concept and language actually exist. So
    # if someone can think of a better solution, I'm here for it!

    # def test_language_has_key_and_lang_exists(self):
    #     """test ThesaurusEntry behaviour with good key and existing structure"""
    #     language = ThesaurusEntry(self.sample["language_key"])
    #
    #     self.assertEqual(language.has_key(), True)
    #     self.assertEqual(language.lang_exists(), True)
    #
    #     language.load_structure(self.sample["structure_key"])
    #     self.assertEqual(language.has_key(), True)

    def test_language_get_concept(self):
        """test concept retrieval of a ThesaurusEntry"""
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
        """test ThesaurusEntry#concept_implemented"""
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
        """test ThesaurusEntry#get_concept_code"""
        language = self.dummy_language

        # Test unknown concept
        self.assertEqual(language.concept_code("12345"), "")

        # Test known concept
        self.assertEqual(language.concept_code("concept1"), "abc")
        self.assertEqual(language.concept_code("concept2"), "abc")
        self.assertEqual(language.concept_code("concept3"), "")
        self.assertEqual(language.concept_code("concept4"), "line1\nline2")

    def test_language_versions(self):
        """test ThesaurusEntry#versions"""
        language = ThesaurusEntry("mysql", "MySQL")
        versions = language.versions()
        self.assertGreater(len(versions), 0)
        self.assertIn("8", versions)

    def test_language_load_filled_concepts(self):
        """test ThesaurusEntry#load_filled_concepts"""
        language = ThesaurusEntry("python", "Python")
        # Python 3 has data_types structure
        response = language.load_filled_concepts("data_types", "3")
        response_json = json.loads(response)
        self.assertEqual(response_json["meta"]["language"], "python")
        self.assertEqual(response_json["meta"]["structure"], "data_types")
        self.assertIn("concepts", response_json)
        # Check if some basic concept exists
        self.assertIn("boolean", response_json["concepts"])

    def test_language_load_comparison(self):
        """test ThesaurusEntry#load_comparison"""
        language = ThesaurusEntry("python", "Python")
        response = language.load_comparison("data_types", "javascript", "ECMAScript 2023", "3")
        response_json = json.loads(response)
        self.assertEqual(response_json["meta"]["entry_1"], "python")
        self.assertEqual(response_json["meta"]["entry_2"], "javascript")
        self.assertIn("concepts1", response_json)
        self.assertIn("concepts2", response_json)

    def test_metainfo_entry_methods(self):
        """test ThesaurusMetaInfo entry related methods"""
        self.assertEqual(self.metainfo.entry_name("python"), "Python")
        lang = self.metainfo.entry("python")
        self.assertIsInstance(lang, ThesaurusEntry)
        self.assertEqual(lang.key, "python")

    def test_metainfo_load_entries(self):
        """test ThesaurusMetaInfo#load_entries"""
        structure = self.metainfo.structure("data_types")
        langs = self.metainfo.load_entries([("python", "3"), ("javascript", "ECMAScript 2023")], structure)
        self.assertEqual(len(langs), 2)
        self.assertEqual(langs[0].key, "python")
        self.assertEqual(langs[1].key, "javascript")

    def test_metainfo_load_entries_missing_structure(self):
        """test ThesaurusMetaInfo#load_entries with missing structure"""
        from web.models import MissingStructureError
        structure = self.metainfo.structure("data_types")
        with self.assertRaises(MissingStructureError) as cm:
            # python 3 definitely has data_types, but let's try something that doesn't exist
            self.metainfo.load_entries([("python", "non_existent_version")], structure)
        
        self.assertEqual(cm.exception.entry_key, "python")
        self.assertEqual(cm.exception.entry_version, "non_existent_version")
