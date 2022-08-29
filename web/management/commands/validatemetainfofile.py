import os
import json
# import sys

from django.core.management.base import BaseCommand, CommandError

from web.models import MetaInfo


class Command(BaseCommand):
    help = "Validate the structure of the meta info file"

    def handle(self, *args, **options):
        error_count = 0
        warning_count = 0
        metainfo = MetaInfo()

        # Look through thesaurus directories, see if any files don't match
        # Load MetaInfo, check directories are in MetaInfo
        meta_files = os.listdir("web/thesauruses/_meta")

        for lang in os.listdir("web/thesauruses"):
            if lang == "_meta":
                continue
            path = "web/thesauruses/" + lang
            if os.path.isdir(path):

                if not lang in list(metainfo.languages):
                    print("[Error] " + path + " exists but " + lang + " is not listed as a language in `meta_info.json`")
                    error_count += 1

                versions = os.listdir(path)
                for version in versions:
                    concepts = os.listdir(path + "/" + version)
                    for concept in concepts:
                        # concept_path = "web/thesauruses/" + lang + "/" + version + concept
                        if concept not in meta_files:
                            print("[Error] `" + path + "` is not a valid concept filename")
                            error_count += 1

        # Check all language directories exist
        for meta_lang in metainfo.languages:
            path = "web/thesauruses/" + meta_lang
            if not os.path.isdir(path):
                print(
                    "[Error] " + metainfo.languages[meta_lang]
                    + " is listed as a language in `meta_info.json` but the directory doesn't exist")
                error_count += 1

        # Check structures are in MetaInfo
        for meta_file in meta_files:
            structure_name = meta_file[:-5]
            if structure_name not in list(metainfo.structures):    # .data_structures.values()):
                print(
                    "[Error] " + "`web/thesauruses/_meta/" + meta_file + "` is not listed as a structure in `meta_info.json`")
                error_count += 1

        # Check all concept files exist in _meta
        for structure in metainfo.structures:
            path = "web/thesauruses/_meta/" + structure + ".json"
            if not os.path.isfile(path):
                print(
                    "[Error] " + structure
                    + " is listed as a structure in `meta_info.json` but the `web/thesauruses/_meta/" + structure + ".json` file doesn't exist")
                error_count += 1


        # if warning_count + error_count > 0:
        if error_count > 0:
            # if warning_count:
            #     print(str(warning_count) + " warnings found.")
            if error_count:
                # print(str(error_count) + " errors found.")
                raise CommandError(str(error_count) + " errors found.")
        else:
            print("No errors found in meta_info.json.")
