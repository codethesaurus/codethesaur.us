import json

from django.test import TestCase

from web.Language import Language
from web.MetaInfo import MetaInfo
from web.MetaStructure import MetaStructure


class TestMetaStructures(TestCase):

	def setUp(self):
		self.metainfo = MetaInfo()
		with open("web/thesauruses/meta_info.json", 'r') as meta_file:
			meta_data = meta_file.read()
		self.data_structures = json.loads(meta_data)["structures"]
		self.languages = json.loads(meta_data)["languages"]

		self.sample_friendly_name = list(self.data_structures.keys())[0]
		self.sample_structure_id = self.data_structures[self.sample_friendly_name]
		self.sample_language_name = list(self.languages.keys())[0]
		self.sample_language_id = self.languages[self.sample_language_name]

	def test_metainfo_structure(self):
		self.assertIsNotNone(self.metainfo)

	def test_metainfo_structure_friendly_name(self):
		test_key = self.metainfo.structure_friendly_name(self.sample_structure_id)

		self.assertEquals(test_key, self.sample_friendly_name)

	def test_metastructure_init(self):
		metastructure = MetaStructure(self.sample_structure_id, self.sample_friendly_name)

		self.assertIsNotNone(metastructure.categories)
		self.assertIsNotNone(metastructure.concepts)

	def test_language_init(self):
		language = Language(self.sample_language_id)

		self.assertIsNotNone(language)
		self.assertIsNotNone(language.key)
		self.assertIsNone(language.friendly_name)
		self.assertIsNone(language.categories)
		self.assertIsNone(language.concepts)

	def test_language_bad_key_and_lang_exists(self):
		bad_language_id = "abcdefg"
		language = Language(bad_language_id)

		self.assertEquals(language.lang_exists(), False)
		self.assertRaises(FileNotFoundError, language.load_structure, bad_language_id)

		self.assertEquals(language.has_key(), True)


	# Commented out as the function *technically* works, but it can't
	# ensure that the sample concept and language actually exist. So
	# if someone can think of a better solution, I'm here for it!

	# def test_language_has_key_and_lang_exists(self):
	# 	language = Language(self.sample_language_id)
	#
	# 	self.assertEquals(language.has_key(), True)
	# 	self.assertEquals(language.lang_exists(), True)
	#
	# 	language.load_structure(self.sample_structure_id)
	# 	self.assertEquals(language.has_key(), True)

	def test_language_get_concept(self):
		language_id = "abcdefg"
		language_friendly_name = "Alphabet language!"

		categories = json.loads("{\"category1\": [\"concept1\",\"concept2\",\"concept3\"]}")
		concepts = json.loads("{\"concept1\": {\"code\": \"abc\"},\"concept2\": {\"code\": \"abc\",\"comment\": \"My comment\"},\"concept3\":{\"not-implemented\": \"true\"}}")

		language = Language(language_id)

		# This is like the manual work of calling language.load_structure()
		language.friendly_name = language_friendly_name
		language.categories = categories
		language.concepts = concepts

		# 	# Test unknown concept
		self.assertEquals(language.concept("12345"), dict({
					"code": "",
					"comment": ""
			}))
		# 	# Test known concept
		self.assertEquals(language.concept("concept1"), dict({"code": "abc"}))
		self.assertEquals(language.concept("concept2"), dict({"code": "abc", "comment": "My comment"}))
		self.assertEquals(language.concept("concept3"), dict({"code": "", "comment": "", "not-implemented": True}))

	def test_language_concept_unknown(self):
		language_id = "abcdefg"
		langauge_friendly_name = "Alphabet language!"

		categories = json.loads("{\"category1\": [\"concept1\",\"concept2\",\"concept3\"]}")
		concepts = json.loads("{\"concept1\": {\"code\": \"abc\"},\"concept2\": {\"code\": \"abc\",\"comment\": \"My comment\"},\"concept3\":{\"not-implemented\": \"true\"}}")

		language = Language(language_id)

		# This is like the manual work of calling language.load_structure()
		language.friendly_name = langauge_friendly_name
		language.categories = categories
		language.concepts = concepts

		# Test unknown concept
		self.assertEquals(language.concept_unknown("12345"), True)
		# Test known concept
		self.assertEquals(language.concept_unknown("concept1"), False)
		self.assertEquals(language.concept_unknown("concept2"), False)
		self.assertEquals(language.concept_unknown("concept3"), False)

	def test_language_concept_implemented(self):
		language_id = "abcdefg"
		langauge_friendly_name = "Alphabet language!"

		categories = json.loads("{\"category1\": [\"concept1\",\"concept2\",\"concept3\"]}")
		concepts = json.loads("{\"concept1\": {\"code\": \"abc\"},\"concept2\": {\"code\": \"abc\",\"comment\": \"My comment\"},\"concept3\":{\"not-implemented\": \"true\"}}")

		language = Language(language_id)

		# This is like the manual work of calling language.load_structure()
		language.friendly_name = langauge_friendly_name
		language.categories = categories
		language.concepts = concepts

		# Test unknown concept
		self.assertEquals(language.concept_implemented("12345"), True)  # Shouldn't this be false

		# Test known concept
		self.assertEquals(language.concept_implemented("concept1"), True)
		self.assertEquals(language.concept_implemented("concept2"), True)
		self.assertEquals(language.concept_implemented("concept3"), False)

	def test_language_get_concept_code(self):
		language_id = "abcdefg"
		langauge_friendly_name = "Alphabet language!"

		categories = json.loads("{\"category1\": [\"concept1\",\"concept2\",\"concept3\"]}")
		concepts = json.loads("{\"concept1\": {\"code\": \"abc\"},\"concept2\": {\"code\": \"abc\",\"comment\": \"My comment\"},\"concept3\":{\"not-implemented\": \"true\"}}")

		language = Language(language_id)

		# This is like the manual work of calling language.load_structure()
		language.friendly_name = langauge_friendly_name
		language.categories = categories
		language.concepts = concepts

		# Test unknown concept
		self.assertEquals(language.concept_code("12345"), "")

		# Test known concept
		self.assertEquals(language.concept_code("concept1"), "abc")
		self.assertEquals(language.concept_code("concept2"), "abc")
		self.assertEquals(language.concept_code("concept3"), "")

	def test_language_get_concept_comment(self):
		language_id = "abcdefg"
		langauge_friendly_name = "Alphabet language!"

		categories = json.loads("{\"category1\": [\"concept1\",\"concept2\",\"concept3\"]}")
		concepts = json.loads("{\"concept1\": {\"code\": \"abc\"},\"concept2\": {\"code\": \"abc\",\"comment\": \"My comment\"},\"concept3\":{\"not-implemented\": \"true\"}}")

		language = Language(language_id)

		# This is like the manual work of calling language.load_structure()
		language.friendly_name = langauge_friendly_name
		language.categories = categories
		language.concepts = concepts

		# Test unknown concept
		self.assertEquals(language.concept_comment("12345"), "")

		# Test known concept
		self.assertEquals(language.concept_comment("concept1"), "")
		self.assertEquals(language.concept_comment("concept2"), "My comment")
		self.assertEquals(language.concept_comment("concept3"), "")

