# Open meta info file
from django.core.management.base import BaseCommand, CommandError
import os

from web.MetaInfo import MetaInfo


class Command(BaseCommand):
    help = "Validates JSON language files with the meta language files"

    def handle(self, *args, **options):
        errors = []

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
                    errors.append(path + " is not listed as a language in meta_info.json")

                files = os.listdir("web/thesauruses/" + dir)
                for f in files:
                    path = "web/thesauruses/" + dir + "/" + f
                    if not f in meta_files:
                        errors.append(path + " is not a valid concept filename")

        # Also check structures are in MetaInfo

        for meta_file in meta_files:
            structure_name = meta_file[:-5]
            if not structure_name in list(metainfo.data_structures.values()):
                errors.append("web/thesauruses/_meta/" + meta_file + " is not listed as a structure in meta_info.json")

        # Open up thesaurus directory
        # language_dirs = os.listdir("web/thesauruses/")
        # for lang_dir in language_dirs:
        #     if os.path.isfile("web/thesauruses/" + lang_dir):
        #         continue

        #    Open up each structures file
        #         structure_files = os.listdir("web/thesauruses/" + lang_dir)



        #       Ensure valid lang/version/name
        #       Ensure categories aren't in file
        #       Ensure name lines are removed
        #       Ensure there's either code or not-implemented
        #       Ensure if not-implemented, there's no code line
        #       Ensure if code, there's no not-implemented
        #       Code can be string or array (maybe warn if string)
        #       There can be a comment
        #       There shouldn't be any other fields
        print(errors)
        print("I'm done!")
