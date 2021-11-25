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

        meta_files = os.listdir("web/thesauruses/_meta")

        for dir in os.listdir("web/thesauruses"):
            if os.path.isdir("web/thesauruses/" + dir):
                files = os.listdir("web/thesauruses/" + dir)
                for f in files:
                    path = "web/thesauruses/" + dir + "/" + f
                    if not f in meta_files:
                        errors.append(path + " is not a valid concept filename")
        print(errors)
        print("I'm done!")
        # Open up thesaurus directory

        #    Open up each concept file
        #       Ensure valid lang/version/name
        #       Ensure categories aren't in file
        #       Ensure name lines are removed
        #       Ensure there's either code or not-implemented
        #       Ensure if not-implemented, there's no code line
        #       Ensure if code, there's no not-implemented
        #       Code can be string or array (maybe warn if string)
        #       There can be a comment
        #       There shouldn't be any other fields
