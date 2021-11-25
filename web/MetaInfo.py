import json
from web.MetaStructure import MetaStructure


class MetaInfo:
    def __init__(self):
        """
        Initializes MetaInfo object with meta language information
        :rtype: None
        """
        with open("web/thesauruses/meta_info.json", 'r') as meta_file:
            meta_data = meta_file.read()
        self.data_structures = json.loads(meta_data)["structures"]
        self.languages = json.loads(meta_data)["languages"]

    def structure_friendly_name(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the structure's human-friendly name
        :param structure_key: ID of the structure located in the meta_info.json file
        :return: string with the human-friendly name
        """
        index = list(self.data_structures.values()).index(structure_key)
        return list(self.data_structures.keys())[index]

    def structure(self, structure_key):
        """
        Given a structure key (from meta_info.json), returns the whole MetaStructure for it
        :param structure_key: ID of the structure located in the meta_info.json file
        :return:
        """
        return MetaStructure(structure_key, self.structure_friendly_name(structure_key))
