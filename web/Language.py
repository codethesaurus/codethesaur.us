import json
import os


class Language:
    def __init__(self, key):
        """
        Initialize the Language object, which will contain concepts for a given structure
        :param key: ID of the language in the meta_info.json file
        """

        # Add an empty string to convert SafeString to str
        self.key = str(key + "")
        self.friendly_name = None
        self.categories = None
        self.concepts = None

    def has_key(self):
        """
        Returns a Boolean if the language key exists or not
        :rtype: bool
        """

        # Empty string is falsy, but text is truthy, but would return return text
        return bool(self.key)

    def lang_exists(self):
        """
        Returns a Boolean if the language (self.key) exists in the thesauruses or not
        :rtype: bool
        """
        return os.path.exists(os.path.join("web", "thesauruses", self.key))

    def load_structure(self, structure_key):
        """
        Loads the structure file into the Language object
        :param structure_key: the ID for the structure to load
        """
        file_path = os.path.join(
            "web", "thesauruses", self.key, structure_key) + ".json"
        with open(file_path, 'r') as file:
            data = file.read()
            # parse file
            file_json = json.loads(data)

            self.friendly_name = file_json["meta"]["language_name"]
            self.categories = file_json["categories"]
            self.concepts = file_json[structure_key]

    def concept(self, concept_key):
        """
        Get the concept (including code and comment) from the concept file for that Lanugage
        :param concept_key: key for the concept to look up
        :returns: a dict containing the code and comment, and possibly the 'not-implemented' flag. They are empty strings if not specified
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
        return self.concept(concept_key).get("not-implemented", False) is False

    def concept_code(self, concept_key):
        """
        Returns the code portion of the provided concept
        :param concept_key: ID for the concept
        :return: the string containing the concept's code
        """
        return self.concept(concept_key).get("code")

    def concept_comment(self, concept_key):
        """
        Returns the comment portion of the provided concept
        :param concept_key: ID for the concept
        :return: the string containing the concept's comment
        """
        return self.concept(concept_key).get("comment", "")

