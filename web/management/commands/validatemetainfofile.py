from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from web.models import MetaInfo


class Command(BaseCommand):
    help = "Validate the structure of the meta info file"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_count = 0
        self.metainfo = None
        self.thesauruses_path = Path("web/thesauruses")
        self.meta_path = self.thesauruses_path / "_meta"

    def handle(self, *args, **options):
        self.metainfo = MetaInfo()
        
        self.check_thesaurus_directories()
        self.check_meta_info_consistency()
        self.check_meta_files_consistency()

        if self.error_count > 0:
            raise CommandError(f"{self.error_count} errors found.")
        
        self.stdout.write(self.style.SUCCESS("No errors found in meta_info.json."))

    def report_error(self, message):
        self.stderr.write(self.style.ERROR(f"[Error] {message}"))
        self.error_count += 1

    def check_thesaurus_directories(self):
        """Look through thesaurus directories, see if any files don't match"""
        meta_files = {f.name for f in self.meta_path.iterdir() if f.is_file()}

        for lang_dir in self.thesauruses_path.iterdir():
            if not lang_dir.is_dir() or lang_dir.name == "_meta":
                continue

            lang = lang_dir.name
            if lang not in self.metainfo.languages:
                self.report_error(f"`{lang_dir}` exists but {lang} is not listed as a language in `meta_info.json`")

            for version_dir in lang_dir.iterdir():
                if version_dir.is_file():
                    self.report_error(f"`{version_dir}` is a file but a directory for a version was expected")
                    continue

                for structure_file in version_dir.iterdir():
                    if structure_file.name not in meta_files:
                        self.report_error(f"`{structure_file}` is not a valid concept filename")

    def check_meta_info_consistency(self):
        """Check all language directories exist for languages listed in meta_info.json"""
        for meta_lang in self.metainfo.languages:
            path = self.thesauruses_path / meta_lang
            if not path.is_dir():
                lang_name = self.metainfo.languages[meta_lang]
                self.report_error(f"{lang_name} is listed as a language in `meta_info.json` but the directory `{path}` doesn't exist")

    def check_meta_files_consistency(self):
        """Check structures in _meta match those in MetaInfo"""
        meta_files = {f.name for f in self.meta_path.iterdir() if f.is_file()}
        
        # Check files in _meta are listed in MetaInfo
        for meta_file in meta_files:
            if not meta_file.endswith(".json"):
                continue
            structure_name = meta_file[:-5]
            if structure_name not in self.metainfo.structures:
                self.report_error(f"`{self.meta_path / meta_file}` is not listed as a structure in `meta_info.json`")

        # Check structures listed in MetaInfo have corresponding files in _meta
        for structure in self.metainfo.structures:
            path = self.meta_path / f"{structure}.json"
            if not path.is_file():
                self.report_error(f"{structure} is listed as a structure in `meta_info.json` but the `{path}` file doesn't exist")
