import json
import os


class MetaStructure:
    def __init__(self, structure_key, friendly_name):
        """
        Inits the MetaStructure object by loading in the concepts and categories from a language's structure file
        :param structure_key: key for the structure
        :param friendly_name: the human-friendly name for the specified structure
        """
        self.key = structure_key
        self.friendly_name = friendly_name
        meta_structure_file_path = os.path.join(
            "web", "thesauruses", "_meta", structure_key) + ".json"
        with open(meta_structure_file_path, 'r') as meta_structure_file:
            data = meta_structure_file.read()
            # parse file
            meta_structure_file_json = json.loads(data)

            self.categories = meta_structure_file_json['categories']
