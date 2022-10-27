import os
import json

from django.core.management.base import BaseCommand, CommandError

from web.models import MetaInfo


class Command(BaseCommand):
    help = "Reads all language JSON files to ensure they're constructed correctly"

    def handle(self, *args, **options):
        error_count = 0
        warning_count = 0

        # Open up thesaurus directory
        language_dirs = os.listdir("web/thesauruses/")
        for lang_dir in language_dirs:
            if lang_dir == "_meta":
                continue
            if os.path.isfile("web/thesauruses/" + lang_dir):
                continue

            # Open up each version directory
            versions = os.listdir("web/thesauruses/" + lang_dir)
            for version in versions:
                #    Open up each structures file
                structure_files = os.listdir("web/thesauruses/" + lang_dir + "/" + version)
                for structure_file in structure_files:
                    structure = structure_file[:-5]

                    #       Ensure valid lang/version/name
                    meta_structure_file_path = os.path.join(
                        "web", "thesauruses", lang_dir, version, structure) + ".json"

                    # parse file
                    with open(meta_structure_file_path, 'r') as meta_structure_file:
                        raw_file_data = meta_structure_file.read()

                        meta_structure_file_json = json.loads(raw_file_data)

                        language = meta_structure_file_json["meta"]["language"]
                        language_version = meta_structure_file_json["meta"]["language_version"]
                        language_name = meta_structure_file_json["meta"]["language_name"]
                        relative_path_name = lang_dir + "/" + version + "/" + structure + ".json"

                        if not language:
                            print(
                                "[Error] `" + relative_path_name + "` has an empty `language` attribute and needs to be updated")
                            error_count += 1
                        elif language == "language_id":
                            print(
                                "[Error] `" + relative_path_name + "` has the default `language` attribute and needs to be updated")
                            error_count += 1
                        elif not language == lang_dir:
                            print(
                                "[Error] `" + relative_path_name + "` has a `language` attribute that should be `" + lang_dir + "` and needs to be updated")
                            error_count += 1

                        if not language_version:
                            print(
                                "[Error] `" + relative_path_name + "` has an empty `language_version` attribute and needs to be updated")
                            error_count += 1
                        elif language_version == "version.number":
                            print(
                                "[Error] `" + relative_path_name + "` has the default `language_version` attribute and needs to be updated")
                            error_count += 1

                        if not language_name:
                            print(
                                "[Error] `" + relative_path_name + "` has an empty `language_name` attribute and needs to be updated")
                            error_count += 1
                        elif language_name == "Human-Friendly Language Name" or language_name == "Human-Readable Language Name":
                            print(
                                "[Error] `" + relative_path_name + "` has the default `language_name` attribute and needs to be updated")
                            error_count += 1

                        #       Ensure categories aren't in file
                        if "categories" in meta_structure_file_json:
                            print(
                                "[Error] `" + relative_path_name + "` has a `categories` section in it, which is now deprecated")
                            error_count += 1

                        #       Ensure name lines are removed
                        for item in meta_structure_file_json["concepts"]:
                            structure_item_data = meta_structure_file_json["concepts"][item]

                            # This generates SO many warnings that I'm commenting it out for now. Consider uncommenting
                            # when more errors and such have been resolved
                            # if "name" in structure_item_data:
                            #     print(
                            #         "[Warn] `" + relative_path_name + "`, ID: `" + item + "` has a `name` line that can be removed")
                            #     warning_count += 1

                            #       Ensure there's either code or not-implemented
                            has_code = "code" in structure_item_data
                            has_not_implemented = "not-implemented" in structure_item_data
                            has_not_underscore_implemented = "not_implemented" in structure_item_data
                            has_comments_plural = "comments" in structure_item_data

                            #       Ensure they use not-implemented (hyphen) not not_implemented (underscore)
                            if has_not_underscore_implemented:
                                print("[Error] `" + relative_path_name + "`, ID: `" + item +
                                      "` has not_implemented (underscore) when it should use not-implemented (hyphen)")
                                error_count += 1

                            if has_code and (has_not_implemented or has_not_underscore_implemented):
                                print(
                                    "[Error] `" + relative_path_name + "`, ID: `" + item + "` should have `code` or `not-implemented`, not both")
                                error_count += 1

                            if not has_code and not has_not_implemented and not has_not_underscore_implemented:
                                print(
                                    "[Error] `" + relative_path_name + "`, ID: `" + item + "` is missing a needed `code` or `not-implemented` line")
                                error_count += 1

                            #       Ensure if not-implemented, there's no code line
                            if has_not_implemented and structure_item_data["not-implemented"] is True and has_code:
                                print("[Error] `" + relative_path_name + "`, ID: `" + item +
                                      "` is not implemented, but has a `code` line that should be removed")
                                error_count += 1

                            #     Ensure if code, it's not empty and there's no not-implemented
                            if has_code and not structure_item_data["code"] and not has_not_implemented:
                                print("[Error] `" + relative_path_name + "`, ID: `" + item +
                                      "` is confusing: `code` is empty but there's no `not-implemented` either")
                                error_count += 1

                            #       Ensure it's comment, not comments
                            if has_comments_plural:
                                print("[Error] `" + relative_path_name + "`, ID: `" + item +
                                      "` has `comments` (plural) that should be `comment` (singular) instead")
                                error_count += 1

                            #       Code can be string or array (maybe warn if string)
                            # if has_code and isinstance(structure_item_data["code"], str):
                                # print("[Warning] `" +
                                #     relative_path_name + "`, ID: `" + item +
                                #     "` has a `code` line that's a string and could optionally be an array")
                                # warning_count += 1

                            #       There shouldn't be any other fields
                            for key in structure_item_data:
                                if not (key == "code"
                                        or key == "comment"
                                        or key == "comments"
                                        or key == "not-implemented"
                                        or key == "not_implemented"
                                        or key == "name"):
                                    # Why "not_implemented"/"name"/"comments"? Because we check for them above, this checks for other exceptions
                                    print("[Warning] `" + relative_path_name + "`, ID: `" + item +
                                          "` has a line `" + key + "` that's unknown")
                                    warning_count += 1

        if warning_count + error_count > 0:
            # if error_count > 0:
            if warning_count:
                print(str(warning_count) + " warnings found.")
            if error_count:
                print(str(error_count) + " errors found.")
                raise CommandError(str(error_count) + " errors found.")
        else:
            print("No issues found.")
