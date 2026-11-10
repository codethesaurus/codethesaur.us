"""Regression tests for issue #826.

The validator previously assumed that the ``concepts`` field of a language file
is always a mapping (dict). When the field is a list, a string, or ``null`` the
command raised an ``AttributeError``. The fix adds a defensive type‑check and
reports an explicit error message instead of crashing.
"""

import os
import shutil
import json
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class ValidatelanginfofilesRegressionTest(TestCase):
    def setUp(self):
        # Create a minimal language structure under ``web/thesauruses/langs``.
        self.base_dir = os.path.join('web', 'thesauruses', 'langs', 'tmp_lang', '1')
        os.makedirs(self.base_dir, exist_ok=True)
        # Path for the file that the validator will process.
        self.file_path = os.path.join(self.base_dir, 'data_types.json')
        # Base meta information – same for all sub‑tests.
        self.meta = {
            "meta": {
                "language": "tmp_lang",
                "language_version": "1",
                "language_name": "Tmp Lang",
            }
        }

    def tearDown(self):
        # Clean up the temporary language directory.
        shutil.rmtree(os.path.join('web', 'thesauruses', 'langs', 'tmp_lang'), ignore_errors=True)

    def _run_validator_and_capture(self):
        """Run the ``validatelanginfofiles`` command and return its stdout.

        The command raises ``CommandError`` when any errors are reported; we
        swallow the exception so the test can still inspect the output.
        """
        out = StringIO()
        try:
            call_command('validatelanginfofiles', stdout=out)
        except Exception:
            # Expected when the validator reports errors.
            pass
        return out.getvalue().lower()

    def test_invalid_concepts_types(self):
        """Check that non‑dict ``concepts`` values are reported as errors.

        The validator should emit an error message of the form:
        ```data_types.json` has a `concepts` section that is not an object``.
        """
        for malformed in [[], "not-a-dict", None]:
            with self.subTest(concepts=type(malformed).__name__):
                # Load the JSON content directly and invoke the command's check_concepts
                content = dict(self.meta)
                content["concepts"] = malformed
                # Instantiate the command and capture its stderr output
                from web.management.commands.validatelanginfofiles import Command
                from pathlib import Path
                cmd = Command()
                # Override output streams so we can capture messages
                from io import StringIO
                cmd.stdout = StringIO()
                cmd.stderr = StringIO()
                # Run only the concepts check (skip other validations)
                cmd.check_concepts(content, Path('data_types.json'))
                output = cmd.stderr.getvalue().lower()
                self.assertIn(
                    "`data_types.json` has a `concepts` section that is not an object",
                    output,
                )
