"""models of codethesaur.us"""
import json
import os


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
            "web", "thesauruses", "_meta", f"{structure_key}.json")
        with open(meta_structure_file_path, 'r', encoding='UTF-8') as meta_structure_file:
            meta_structure_file_json = json.load(meta_structure_file)

            self.categories = meta_structure_file_json["categories"]


class Language:
    """
    Represents a programming language and knows how to fetch concepts for a
    structure key
    """

    def __init__(self, key, friendly_name):
        """
        Initialize the Language object, which will contain concepts for a given
        structure

        :param key: ID of the language in the meta_info.json file
        """

        # Add an empty string to convert SafeString to str
        self.key = str(key + "")
        self.friendly_name = friendly_name
        self.concepts = None
        self.language_dir = os.path.join("web", "thesauruses", self.key)
        self.version = None


    def versions(self):
        """Generate all versions and their paths for the Language"""
        versions = dict()
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
        return os.path.exists(self.language_dir)

    def load_concepts(self, structure_key, version):
        """
        Loads the structure file into the Language object

        :param structure_key: the ID for the structure to load
        :param version: the version of the language
        """
        file_path = os.path.join(self.language_dir, version, f"{structure_key}.json")
        with open(file_path, 'r', encoding='UTF-8') as file:
            file_json = json.load(file)
            self.concepts = file_json["concepts"]
        self.version = version


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


class MissingLanguageError(Exception):
    """Error for when a requested language is not defined in `meta.json`"""
    def __init__(self, key):
        super().__init__()
        self.key = key


class MissingStructureError(Exception):
    """
    Error that signals that a specific language & version does not have the structure
    defined
    """
    def __init__(self, structure, language_key, language_name, language_version):
        super().__init__()
        self.structure = structure
        self.language_key = language_key
        self.language_name = language_name
        self.language_version = language_version


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

    def language(self, language_key):
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
        )


    def load_languages(self, language_keys_versions, meta_structure):
        """Tries to load all languages from `language_keys` and the requested `structure`"""
        languages = []
        for language_key, version in language_keys_versions:
            try:
                language = self.language(language_key)
                version = version or sorted(language.versions())[-1]
                language.load_concepts(meta_structure.key, version)
                languages.append(language)
            except FileNotFoundError as file_not_found:
                raise MissingStructureError(
                    meta_structure,
                    language_key,
                    self.language_friendly_name(language_key),
                    version,
                ) from file_not_found
            except KeyError as key_error:
                raise MissingLanguageError(language_key) from key_error
        return languages


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
