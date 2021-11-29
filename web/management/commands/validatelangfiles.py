import os
import json

from django.core.management.base import BaseCommand, CommandError
from web.MetaInfo import MetaInfo


class Command(BaseCommand):
    help = "Reads all language JSON files to ensure they're constructed correctly"

    def handle(self, *args, **options):
        error_count = 0
        warning_count = 0
        metainfo = MetaInfo()

        # Look though thesaurus directories, see if any files don't match
        # Load MetaInfo, check directories are in MetaInfo
        meta_files = os.listdir("web/thesauruses/_meta")

        for dir in os.listdir("web/thesauruses"):
            if dir == "_meta":
                continue
            path = "web/thesauruses/" + dir
            if os.path.isdir(path):

                if not dir in list(metainfo.languages.values()):
                    print("[Error] " +path + " is not listed as a language in `meta_info.json`")
                    error_count += 1

                files = os.listdir("web/thesauruses/" + dir)
                for file in files:
                    path = "web/thesauruses/" + dir + "/" + file
                    if file not in meta_files:
                        print("[Error] `" +path + "` is not a valid concept filename")
                        error_count += 1

        # Also check structures are in MetaInfo
        for meta_file in meta_files:
            structure_name = meta_file[:-5]
            if structure_name not in list(metainfo.data_structures.values()):
                print("[Error] " +"`web/thesauruses/_meta/" + meta_file + "` is not listed as a structure in `meta_info.json`")
                error_count += 1

        # Open up thesaurus directory
        language_dirs = os.listdir("web/thesauruses/")
        for lang_dir in language_dirs:
            if lang_dir == "_meta":
                continue
            if os.path.isfile("web/thesauruses/" + lang_dir):
                continue

            #    Open up each structures file
            structure_files = os.listdir("web/thesauruses/" + lang_dir)
            for structure_file in structure_files:
                structure = structure_file[:-5]

                #       Ensure valid lang/version/name
                meta_structure_file_path = os.path.join(
                    "web", "thesauruses", lang_dir, structure) + ".json"
                # parse file
                with open(meta_structure_file_path, 'r') as meta_structure_file:
                    raw_file_data = meta_structure_file.read()

                    meta_structure_file_json = json.loads(raw_file_data)

                    language = meta_structure_file_json["meta"]["language"]
                    language_version = meta_structure_file_json["meta"]["language_version"]
                    language_name = meta_structure_file_json["meta"]["language_name"]
                    if not language:
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has an empty `language` attribute and needs to be updated")
                        error_count += 1
                    elif language == "language_id":
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has the default `language` attribute and needs to be updated")
                        error_count += 1
                    elif not language == lang_dir:
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has a `language` attribute that should be `" + lang_dir + "` and needs to be updated")
                        error_count += 1

                    if not language_version:
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has an empty `language_version` attribute and needs to be updated")
                        error_count += 1
                    elif language_version == "version.number":
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has the default `language_version` attribute and needs to be updated")
                        error_count += 1

                    if not language_name:
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has an empty `language_name` attribute and needs to be updated")
                        error_count += 1
                    elif language_name == "Human-Friendly Language Name":
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has the default `language_name` attribute and needs to be updated")
                        error_count += 1

                    #       Ensure categories aren't in file
                    if "categories" in meta_structure_file_json:
                        print("[Error] `" +
                            lang_dir + "/" + structure + ".json` has a `categories` section in it, which are no longer needed in language files")
                        error_count += 1

                    #       Ensure name lines are removed
                    for item in meta_structure_file_json[structure]:
                        structure_item_data = meta_structure_file_json[structure][item]

                        if "name" in structure_item_data:
                            print("[Error] `" +
                                lang_dir + "/" + structure + ".json`, ID: `" + item + "` has a `name` line that can be removed")
                            error_count += 1

                        #       Ensure there's either code or not-implemented
                        has_code = "code" in structure_item_data
                        has_not_implemented = "not-implemented" in structure_item_data
                        has_comment = "comment" in structure_item_data
                        if (has_code and has_not_implemented):
                            print("[Error] `" +
                                lang_dir + "/" + structure + ".json`, ID: `" + item + "` should have `code` or `not-implemented`, not both")
                            error_count += 1
                        elif (not has_code and not has_not_implemented):
                            print("[Error] `" +
                                lang_dir + "/" + structure + ".json`, ID: `" + item + "` is missing a needed `code` or `not-implemented` line")
                            error_count += 1
                        #       Ensure if not-implemented, there's no code line
                        elif has_not_implemented and structure_item_data["not-implemented"] is True and has_code:
                            print("[Error] `" +
                                lang_dir + "/" + structure + ".json`, ID: `" + item +
                                "` is not implemented, but has a `code` line that should be removed")
                            error_count += 1
                        #       Ensure if code, there's no not-implemented
                        elif has_code and not structure_item_data["code"] and not has_not_implemented:
                            print("[Error] `" +
                                lang_dir + "/" + structure + ".json`, ID: `" + item +
                                "` has an empty `code` line but doesn't have `not-implemented` instead")
                            error_count += 1

                        #       Code can be string or array (maybe warn if string)
                        elif has_code and isinstance(structure_item_data["code"], str):
                            # print("[Warning] `" +
                            #     lang_dir + "/" + structure + ".json`, ID: `" + item +
                            #     "` has a `code` line that's a string and could optionally be an array")
                            warning_count += 1

                        #       There shouldn't be any other fields
                        for key in structure_item_data:
                            if not (key == "code" or key == "comment" or key == "not-implemented"):
                                # print("[Warning] `" +
                                #     lang_dir + "/" + structure + ".json`, ID: `" + item +
                                #     "` has a line `" + key + "` that's unknown")
                                warning_count += 1
        # if warning_count + error_count > 0:
        if error_count > 0:
            # if warning_count:
            #     print(str(warning_count) + " warnings found.")
            if error_count:
                raise CommandError(str(error_count) + " errors found.")