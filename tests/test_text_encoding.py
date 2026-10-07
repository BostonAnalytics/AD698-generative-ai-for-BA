import unittest

from scripts.check_text_encoding import violations


class TextEncodingTests(unittest.TestCase):
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
