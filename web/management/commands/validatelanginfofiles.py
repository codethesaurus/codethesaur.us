import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Reads all language JSON files to ensure they're constructed correctly"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_count = 0
        self.warning_count = 0
        self.thesauruses_path = Path("web/thesauruses")

    def handle(self, *args, **options):
        for lang_dir in self.thesauruses_path.iterdir():
            if not lang_dir.is_dir() or lang_dir.name == "_meta":
                continue

            for version_dir in lang_dir.iterdir():
                if not version_dir.is_dir():
                    continue

                for structure_file in version_dir.glob("*.json"):
                    self.validate_language_file(structure_file)

        if self.warning_count > 0:
            self.stdout.write(self.style.WARNING(f"{self.warning_count} warnings found."))

        if self.error_count > 0:
            self.stdout.write(self.style.ERROR(f"{self.error_count} errors found."))
            raise CommandError(f"{self.error_count} errors found.")

        if self.error_count == 0 and self.warning_count == 0:
            self.stdout.write(self.style.SUCCESS("No issues found."))

    def report_error(self, message):
        self.stderr.write(self.style.ERROR(f"[Error] {message}"))
        self.error_count += 1

    def report_warning(self, message):
        self.stdout.write(self.style.WARNING(f"[Warning] {message}"))
        self.warning_count += 1

    def validate_language_file(self, file_path):
        relative_path = file_path.relative_to(self.thesauruses_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.report_error(f"Failed to parse `{relative_path}`: {e}")
            return

        self.check_meta_section(data, relative_path)
        self.check_concepts(data, relative_path)

    def check_meta_section(self, data, relative_path):
        meta = data.get("meta", {})
        # relative_path is something like "python/3/data_types.json"
        # parts[0] is the language directory name
        lang_dir = relative_path.parts[0]

        language = meta.get("language")
        language_version = meta.get("language_version")
        language_name = meta.get("language_name")

        if not language:
            self.report_error(f"`{relative_path}` has an empty `language` attribute and needs to be updated")
        elif language == "language_id":
            self.report_error(f"`{relative_path}` has the default `language` attribute and needs to be updated")
        elif language != lang_dir:
            self.report_error(f"`{relative_path}` has a `language` attribute that should be `{lang_dir}` and needs to be updated")

        if not language_version:
            self.report_error(f"`{relative_path}` has an empty `language_version` attribute and needs to be updated")
        elif language_version == "version.number":
            self.report_error(f"`{relative_path}` has the default `language_version` attribute and needs to be updated")

        if not language_name:
            self.report_error(f"`{relative_path}` has an empty `language_name` attribute and needs to be updated")
        elif language_name in ["Human-Friendly Language Name", "Human-Readable Language Name"]:
            self.report_error(f"`{relative_path}` has the default `language_name` attribute and needs to be updated")

        if "categories" in data:
            self.report_error(f"`{relative_path}` has a `categories` section in it, which is now deprecated")

    def check_concepts(self, data, relative_path):
        concepts = data.get("concepts", {})
        for concept_id, item_data in concepts.items():
            has_code = "code" in item_data
            has_not_implemented = "not-implemented" in item_data
            has_not_underscore_implemented = "not_implemented" in item_data
            has_comments_plural = "comments" in item_data

            if has_not_underscore_implemented:
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` has not_implemented (underscore) "
                    "when it should use not-implemented (hyphen)"
                )

            if has_code and (has_not_implemented or has_not_underscore_implemented):
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` should have `code` or `not-implemented`, not both"
                )

            if not has_code and not has_not_implemented and not has_not_underscore_implemented:
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` is missing a needed `code` or `not-implemented` line"
                )

            if has_not_implemented and item_data.get("not-implemented") is True and has_code:
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` is not implemented, but has a `code` line that should be removed"
                )

            if has_code and not item_data.get("code") and not has_not_implemented:
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` is confusing: `code` is empty but there's no `not-implemented` either"
                )

            if has_comments_plural:
                self.report_error(
                    f"`{relative_path}`, ID: `{concept_id}` has `comments` (plural) that should be `comment` (singular) instead"
                )

            # Check for unknown keys
            allowed_keys = {"code", "comment", "not-implemented", "not_implemented", "name", "comments"}
            for key in item_data:
                if key not in allowed_keys:
                    self.report_warning(f"`{relative_path}`, ID: `{concept_id}` has a line `{key}` that's unknown")
