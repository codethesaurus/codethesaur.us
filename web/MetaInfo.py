import json
import os
from web.MetaStructure import MetaStructure


class MetaInfo:
    def __init__(self):
        """
        Initializes MetaInfo object with meta language information
        :rtype: None
        """
        meta_info_file_path = os.path.join(
            "web", "thesauruses", "meta_info.json")
        with open(meta_info_file_path, 'r') as meta_file:
            meta_data = meta_file.read()
        meta_info_json = json.loads(meta_data)
        self.data_structures = meta_info_json["structures"]
        self.languages = meta_info_json["languages"]

    def language_friendly_name(self, language_key):
        """
        Given a structure key (from meta_info.json), returns the language's human-friendly name
        :param language_key: ID of the language located in the meta_info.json file
        :return: string with the human-friendly name
        """
        return self.languages[language_key]["name"]

    def structure_friendly_name(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the structure's human-friendly name
        :param structure_key: ID of the structure located in the meta_info.json file
        :return: string with the human-friendly name
        """
        return self.data_structures[structure_key]

    def structure(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the whole MetaStructure for it
        :param structure_key: ID of the structure located in the meta_info.json file
        :return:
        """
        return MetaStructure(structure_key, self.structure_friendly_name(structure_key))
