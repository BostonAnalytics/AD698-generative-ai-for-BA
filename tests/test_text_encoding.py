import unittest
import contextlib
import io
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts import check_text_encoding
from scripts.check_text_encoding import violations


class TextEncodingTests(unittest.TestCase):
    def test_discovery_skips_deleted_files_and_checks_existing_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = ["tracked.qmd", "new.md", "M4/M04_P1_files/figure-revealjs/missing.svg"]
            (root / names[0]).write_text("valid", encoding="utf-8")
            (root / names[1]).write_text("invalid \ufffd", encoding="utf-8")
            with patch.object(check_text_encoding, "ROOT", root), patch.object(
                check_text_encoding.subprocess, "check_output",
                return_value=("\0".join(names) + "\0").encode("utf-8"),
            ), patch.object(check_text_encoding.sys, "argv", ["check_text_encoding.py"]):
                self.assertEqual(check_text_encoding.source_files(), [root / name for name in names[:2]])
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertTrue(check_text_encoding.main())
                self.assertIn("possible corrupted text", output.getvalue())

    def test_explicit_missing_path_reports_failure_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.svg")
            with patch.object(check_text_encoding.sys, "argv", ["check_text_encoding.py", missing]):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertTrue(check_text_encoding.main())
                self.assertIn("cannot read file", output.getvalue())

    def test_rejects_reported_corruption(self):
        for symbol in ("\U0001f4ca", "\u00b2", "\u00d7", "\u2014", "\u2019"):
            broken = symbol.encode("utf-8").decode("cp1252")
            with self.subTest(symbol=symbol):
                self.assertTrue(violations(broken))

    def test_preserves_legitimate_unicode(self):
        self.assertEqual(violations("R\u00b2; 28\u00d728; caf\u00e9; \u201cquote\u201d; \u03b1 \u2192 \u03b2; \U0001f4ca"), [])

    def test_reports_line_and_replacement_character(self):
        self.assertEqual(violations("valid\ninvalid \ufffd")[0][0], 2)


if __name__ == "__main__":
    unittest.main()
