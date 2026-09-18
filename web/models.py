"""models of codethesaur.us"""
import json
import os
from jsonmerge import merge

from django.db import models


def _is_safe_path_component(value):
    return bool(value) and value not in (
        os.curdir, os.pardir
    ) and "/" not in value and "\\" not in value


# pylint: disable=too-few-public-methods
class MetaStructure:
    """
    Holds info about how the structure is divided into categories and
    concepts
    """
    _cached_files = {}

    def __init__(self, key, name):
        """
        Inits the MetaStructure object by loading in the concepts and
        categories from a language's structure file

        :param key: key for the structure
        :param name: the human-friendly name for the specified structure
        """
        self.key = key
        self.name = name

        if not _is_safe_path_component(key):
            raise FileNotFoundError(f"Structure key is not a safe path component: {key!r}")

        if key in MetaStructure._cached_files:
            self.categories = MetaStructure._cached_files[key]
            return

        thesaurus_root = os.path.join("web", "thesauruses")
        root_real = os.path.realpath(thesaurus_root)
        meta_structure_file_path = os.path.realpath(
            os.path.join(thesaurus_root, "_meta", f"{key}.json"))
        if not meta_structure_file_path.startswith(root_real + os.sep):
            raise FileNotFoundError(f"Structure key escapes the thesaurus dir: {key!r}")
        with open(meta_structure_file_path, 'r', encoding='UTF-8') as meta_structure_file:
            meta_structure_file_json = json.load(meta_structure_file)

            self.categories = meta_structure_file_json["categories"]
            MetaStructure._cached_files[key] = self.categories


class ThesaurusEntry:
    """
    Represents a programming language and knows how to fetch concepts for a
    structure key
    """

    def __init__(self, key, name):
        """
        Initialize the ThesaurusEntry object, which will contain concepts for a given
        structure

        :param key: key of the language in the meta_info.json file
        :param name: the human-friendly name for the specified language
        """

        # Add an empty string to convert SafeString to str
        self.key = str(key + "")
        self.name = name
        self.concepts = None
        self.version = None
        self.language_dir = None
        if not _is_safe_path_component(self.key):
            return

        thesaurus_root = os.path.join("web", "thesauruses")
        root_real = os.path.realpath(thesaurus_root)
        for category in os.listdir(thesaurus_root):
            if category == "_meta" or not os.path.isdir(os.path.join(thesaurus_root, category)):
                continue
            potential_dir = os.path.realpath(
                os.path.join(thesaurus_root, category, self.key))
            if potential_dir.startswith(root_real + os.sep) and os.path.isdir(potential_dir):
                self.language_dir = potential_dir
                break
        
        if self.language_dir is None:
            fallback_dir = os.path.realpath(
                os.path.join(thesaurus_root, "langs", self.key))
            if fallback_dir.startswith(root_real + os.sep):
                self.language_dir = fallback_dir
        self.version = None


    def versions(self):
        """Generate all versions and their paths for the ThesaurusEntry"""
        versions = dict()
        if self.language_dir is None:
            return versions
        try:
            for entry in os.scandir(self.language_dir):
                if not entry.is_dir():
                    continue

                file_version = os.path.basename(entry.path)
                versions[file_version] = entry.path
        except FileNotFoundError:
            pass

        return versions


    def __bool__(self):
        """
        Returns a Boolean if the language (self.key) exists in the thesauruses
        or not

        :rtype: bool
        """
        return self.language_dir is not None and os.path.exists(self.language_dir)

    def load_concepts(self, structure_key, version):
        """
        Loads the structure file into the ThesaurusEntry object

        :param structure_key: the key for the structure to load
        :param version: the version of the language
        """
        if not (_is_safe_path_component(structure_key) and _is_safe_path_component(version)):
            raise FileNotFoundError(
                f"Unsafe structure/version path components: {structure_key!r} / {version!r}")
        root_real = os.path.realpath(os.path.join("web", "thesauruses"))
        file_path = os.path.realpath(os.path.join(
            self.language_dir, version, f"{structure_key}.json"))
        if not file_path.startswith(root_real + os.sep):
            raise FileNotFoundError(
                f"Structure/version escape the thesaurus dir: {structure_key!r} / {version!r}")
        with open(file_path, 'r', encoding='UTF-8') as file:
            file_json = json.load(file)
            self.concepts = file_json["concepts"]
        self.version = version

    def load_filled_concepts(self, structure_key, version):
        from web.thesaurus_template_generators import generate_entry_template
        """
        Loads the concepts from the entry's structure file

        :param structure_key: the ID for the concept to load
        :param version: the version of the entry
        :return: a dict containing the code and comment, and possibly the
            'not-implemented' flag. They are empty code entries if not specified
        :rtype: object Filled template
        """

        self.load_concepts(structure_key, version)

        template = generate_entry_template(
            self.key,
            structure_key,
            version
        )

        template = json.loads(template)

        template['concepts'] = merge(template['concepts'], self.concepts)

        response = json.dumps(template, indent=2)

        return response

    def load_comparison(self, structure_key, entry_key, version_entry, version_self):
        entry_obj = ThesaurusEntry(entry_key, "")
        self_filled_concept = self.load_filled_concepts(structure_key, version_self)
        entry_filled_concept = entry_obj.load_filled_concepts(structure_key, version_entry)

        if self_filled_concept is False or entry_filled_concept is False:
            return False

        response = json.dumps({
            "meta": {
                "entry_1": self.key,
                "entry_version_1": version_self,
                "entry_2": entry_obj.key,
                "entry_version_2": version_entry,
                "structure": structure_key
            },
            "concepts1": json.loads(self_filled_concept)['concepts'],
            "concepts2": json.loads(entry_filled_concept)['concepts']
        }, indent=2)

        return response


    def concept(self, concept_key):
        """
        Get the concept (including code and comment) from the concept file for
        that ThesaurusEntry

        :param concept_key: key for the concept to look up
        :returns: a dict containing the code and comment, and possibly the
            'not-implemented' flag. They are empty strings if not specified
        :rtype: object
        """
        if self.concepts.get(concept_key) is None:
            return {
                "code": "",
                "comment": ""
            }
        if self.concepts.get(concept_key).get("not-implemented", False):
            return {
                "not-implemented": True,
                "code": "",
                "comment": self.concepts.get(concept_key).get("comment", "")
            }
        return self.concepts.get(concept_key)

    def concept_unknown(self, concept_key):
        """
        Returns a Boolean if the concept is not known

        :param concept_key: key for the concept
        :return: Boolean if the concept is not known
        """
        return self.concepts.get(concept_key) is None

    def concept_implemented(self, concept_key):
        """
        Returns a Boolean if the concept is implemented

        :param concept_key: key for the concept
        :return: Boolean if the language defines this concept
        """
        return not self.concept(concept_key).get("not-implemented", False)

    def concept_code(self, concept_key):
        """
        Returns the code portion of the provided concept

        :param concept_key: key for the concept
        :return: the string containing the concept's code
        """
        code = self.concept(concept_key).get("code")
        if isinstance(code, list):
            code = "\n".join(code)
        return code

    def concept_comment(self, concept_key):
        """
        Returns the comment portion of the provided concept

        :param concept_key: key for the concept
        :return: the string containing the concept's comment
        """
        comment = self.concept(concept_key).get("comment", "")
        if isinstance(comment, list):
            comment = "\n".join(comment)
        return comment


    def is_concept_complete(self, concept_key):
        """
        Returns a Boolean if the concept has either code or a comment.
        """
        if self.concept_unknown(concept_key):
            return False
        if not self.concept_implemented(concept_key):
            return True # If explicitly marked as not-implemented, we consider it "complete" in terms of knowledge
        return bool(self.concept_code(concept_key) or self.concept_comment(concept_key))

    def is_category_incomplete(self, category_concepts_keys):
        """
        Returns a Boolean if ANY concept in the category is unknown or missing code/comment.
        """
        for key in category_concepts_keys:
            if self.concept_unknown(key):
                return True
            if self.concept_implemented(key) and not (self.concept_code(key) or self.concept_comment(key)):
                return True
        return False

    def has_any_implemented_in_category(self, category_concepts_keys):
        """
        Returns True if at least one concept in the category is known AND implemented.
        """
        for key in category_concepts_keys:
            if not self.concept_unknown(key) and self.concept_implemented(key):
                return True
        return False


class MissingEntryError(Exception):
    """Error for when a requested entry is not defined in `meta.json`"""
    def __init__(self, key):
        super().__init__()
        self.key = key


class MissingStructureError(Exception):
    """
    Error that signals that a specific entry & version does not have the structure
    defined
    """
    def __init__(self, structure, entry_key, entry_name, entry_version):
        super().__init__()
        self.structure = structure
        self.entry_key = entry_key
        self.entry_name = entry_name
        self.entry_version = entry_version


class ThesaurusMetaInfo:
    """Holds info about structures and languages"""
    _cached_structures = None
    _cached_languages = None

    def __init__(self):
        """
        Initializes ThesaurusMetaInfo object with meta language information

        :rtype: None
        """
        if ThesaurusMetaInfo._cached_structures is not None:
            self.structures = ThesaurusMetaInfo._cached_structures
            self.languages = ThesaurusMetaInfo._cached_languages
            self.categories = getattr(ThesaurusMetaInfo, "_cached_categories", {})
            self.category_structures = getattr(ThesaurusMetaInfo, "_cached_category_structures", {})
            return

        meta_info_file_path = os.path.join(
            "web", "thesauruses", "meta_info.json")
        with open(meta_info_file_path, 'r', encoding='UTF-8') as meta_file:
            meta_info_json = json.load(meta_file)
        
        self.categories = meta_info_json.get("categories", {})
        self.languages = meta_info_json["languages"]
        
        # Flatten structures for backward compatibility where needed, 
        # but keep track of category-specific ones
        self.category_structures = meta_info_json["structures"]
        self.structures = {}
        for cat_structs in self.category_structures.values():
            self.structures.update(cat_structs)

        ThesaurusMetaInfo._cached_structures = self.structures
        ThesaurusMetaInfo._cached_languages = self.languages
        ThesaurusMetaInfo._cached_categories = self.categories
        ThesaurusMetaInfo._cached_category_structures = self.category_structures
        

    def entry_name(self, entry_key):
        """
        Given a structure key (from meta_info.json), returns the entry's human-friendly name

        :param entry_key: key of the entry located in the meta_info.json file
        :return: string with the human-friendly name
        """
        return self.languages[entry_key]

    def entry(self, entry_key):
        """
        Given a entry key (from meta_info.json), returns the whole
        ThesaurusEntry for it

        :param entry_key: key of the entry located in the meta_info.json
            file
        :return: ThesaurusEntry for the requested key
        :rtype: ThesaurusEntry
        """
        return ThesaurusEntry(
            entry_key,
            self.entry_name(entry_key),
        )


    def load_entries(self, entry_keys_versions, meta_structure):
        """Tries to load all entries from `entry_keys` and the requested `structure`"""
        entries = []
        for entry_key, version in entry_keys_versions:
            try:
                entry = self.entry(entry_key)
                version = version or sorted(entry.versions())[-1]
                entry.load_concepts(meta_structure.key, version)
                entries.append(entry)
            except FileNotFoundError as file_not_found:
                raise MissingStructureError(
                    meta_structure,
                    entry_key,
                    self.entry_name(entry_key),
                    version,
                ) from file_not_found
            except KeyError as key_error:
                raise MissingEntryError(entry_key) from key_error
        return entries


    def structure_name(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the structure's
        human-friendly name

        :param structure_key: key of the structure located in the meta_info.json
            file
        :return: string with the human-friendly name
        :rtype: String
        """
        return self.structures[structure_key]

    def structure(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the whole
        MetaStructure for it

        :param structure_key: key of the structure located in the meta_info.json
            file
        :return: MetaStructure for the requested key
        :rtype: MetaStructure
        """
        return MetaStructure(
            structure_key,
            self.structure_name(structure_key)
        )

class SiteVisit(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=300)
    user_agent = models.CharField(max_length=300)
    referer = models.CharField(max_length=300)


class LookupData(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    entry1 = models.CharField(max_length=50)
    version1 = models.CharField(max_length=20, default='')
    entry2 = models.CharField(max_length=50)
    version2 = models.CharField(max_length=20, default='')
    structure = models.CharField(max_length=50)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)


class MissingLookup(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)
    item_type = models.CharField(max_length=20)  # 'language', 'structure', 'concept'
    item_value = models.CharField(max_length=100)
    language_context = models.CharField(max_length=50, blank=True, null=True)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)
