"""models of codethesaur.us"""
import json
import os
from packaging.version import parse as parse_version


# pylint: disable=too-few-public-methods
class MetaStructure:
    """
    Holds info about how the structure is divided into categories and
    concepts
    """

    def __init__(self, structure_key, friendly_name):
        """
        Inits the MetaStructure object by loading in the concepts and
        categories from a language's structure file

        :param structure_key: key for the structure
        :param friendly_name: the human-friendly name for the specified
            structure
        """
        self.key = structure_key
        self.friendly_name = friendly_name
        meta_structure_file_path = os.path.join(
            "web", "thesauruses", "_meta", structure_key) + ".json"
        with open(meta_structure_file_path, 'r', encoding='UTF-8') as meta_structure_file:
            meta_structure_file_json = json.load(meta_structure_file)

            self.categories = meta_structure_file_json["categories"]

class StructureFileNotFound(Exception):
    """Thrown if `Language` could not find any structure file"""

class Language:
    """
    Represents a programming language and knows how to fetch concepts for a
    structure key
    """

    def __init__(self, key, friendly_name, version = None):
        """
        Initialize the Language object, which will contain concepts for a given
        structure

        :param key: ID of the language in the meta_info.json file
        :param version: the version of the language requested
        """

        # Add an empty string to convert SafeString to str
        self.key = str(key + "")
        self.friendly_name = friendly_name
        self.concepts = dict()
        if version is not None:
            version = parse_version(version)
        self.language_dir_name = os.path.join("web", "thesauruses", self.key)

        self.versions = dict()
        try:
            for entry in os.scandir(self.language_dir_name):
                if not entry.is_dir():
                    continue

                file_version_string = os.path.basename(entry.path)
                file_version = parse_version(file_version_string)
                if version is None or file_version < version:
                    self.versions[file_version] = entry.path
        except FileNotFoundError:
            pass

    def __bool__(self):
        """
        Returns a Boolean if the language (self.key) exists in the thesauruses
        or not

        :rtype: bool
        """
        return os.path.exists(os.path.join("web", "thesauruses", self.key))

    def load_concepts(self, structure_key):
        """
        Loads the structure file(s) into the Language object

        :param structure_key: the ID for the structure to load
        """

        found_any = False
        structure_file_name = f"{structure_key}.json"
        versions = dict(self.versions)
        # fallback to the base directory
        versions[parse_version("default")] = self.language_dir_name
        for version in sorted(versions):
            structure_file_path = os.path.join(versions.get(version), structure_file_name)

            try:
                with open(structure_file_path, 'r', encoding='UTF-8') as structure_file:
                    structure_json = json.load(structure_file)
            except FileNotFoundError:
                continue

            found_any = True
            structure_concepts = structure_json["concepts"]
            for concept in structure_json["concepts"]:
                self.concepts[concept] = structure_concepts[concept]
                self.concepts[concept]["version"] = version

        if not found_any:
            raise StructureFileNotFound


    def concept(self, concept_key):
        """
        Get the concept (including code and comment) from the concept file for
        that Language

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

        :param concept_key: ID for the concept
        :return: Boolean if the concept is not known
        """
        return self.concepts.get(concept_key) is None

    def concept_implemented(self, concept_key):
        """
        Returns a Boolean if the concept is implemented

        :param concept_key: ID for the concept
        :return: Boolean if the language defines this concept
        """
        return not self.concept(concept_key).get("not-implemented", False)

    def concept_code(self, concept_key):
        """
        Returns the code portion of the provided concept

        :param concept_key: ID for the concept
        :return: the string containing the concept's code
        """
        code = self.concept(concept_key).get("code")
        if isinstance(code, list):
            code = "\n".join(code)
        return code

    def concept_comment(self, concept_key):
        """
        Returns the comment portion of the provided concept

        :param concept_key: ID for the concept
        :return: the string containing the concept's comment
        """
        return self.concept(concept_key).get("comment", "")


class MetaInfo:
    """Holds info about structures and languages"""

    def __init__(self):
        """
        Initializes MetaInfo object with meta language information

        :rtype: None
        """
        meta_info_file_path = os.path.join(
            "web", "thesauruses", "meta_info.json")
        with open(meta_info_file_path, 'r', encoding='UTF-8') as meta_file:
            meta_info_json = json.load(meta_file)
        self.structures = meta_info_json["structures"]
        self.languages = meta_info_json["languages"]

    def language_friendly_name(self, language_key):
        """
        Given a structure key (from meta_info.json), returns the language's human-friendly name

        :param language_key: ID of the language located in the meta_info.json file
        :return: string with the human-friendly name
        """
        return self.languages[language_key]

    def language(self, language_key, version = None):
        """
        Given a language key (from meta_info.json), returns the whole
        Language for it

        :param language_key: ID of the language located in the meta_info.json
            file
        :return: Language for the requested key
        :rtype: Language
        """
        return Language(
            language_key,
            self.language_friendly_name(language_key),
            version
        )

    def structure_friendly_name(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the structure's
        human-friendly name

        :param structure_key: ID of the structure located in the meta_info.json
            file
        :return: string with the human-friendly name
        :rtype: String
        """
        return self.structures[structure_key]

    def structure(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the whole
        MetaStructure for it

        :param structure_key: ID of the structure located in the meta_info.json
            file
        :return: MetaStructure for the requested key
        :rtype: MetaStructure
        """
        return MetaStructure(
            structure_key,
            self.structure_friendly_name(structure_key)
        )
