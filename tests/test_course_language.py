import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_course_language.py"
SPEC = importlib.util.spec_from_file_location("course_language", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class CourseLanguageTests(unittest.TestCase):
    def test_reported_leaks_and_wrapped_variants_fail(self):
        for text in (
            "This sets the stage for neural models.",
            "This will set the intuition for students.",
            "It will make a good example.",
            "THIS **SETS**\nthe stage for neural models.",
            "This would make a useful example.",
            "Two examples are useful in lecture because students can inspect every word.",
            "This is a useful place to pause in lecture and ask students why.",
            "Students should hear the line explicitly.",
            "A second narrative improvement is to explicitly say this.",
            "This is a strong teaching activation.",
            "For classroom narrative, this is much more memorable.",
            "This is a useful mental model for teaching HNSW.",
            "This story works especially well when teaching business applications.",
            "This is useful for class because it moves students away from that idea.",
            "The comparison is helpful pedagogically.",
            "A narrative correction for students is to stop introducing networks this way.",
        ):
            with self.subTest(text=text):
                self.assertTrue(checker.violations(text))

    def test_hidden_authoring_text_is_not_a_bypass(self):
        for text in (
            "::: {.notes}\nThis sets the stage for neural models.\n:::",
            "<!-- It will make a good example. -->",
            '![This will set the intuition for students.](figure.svg)',
        ):
            with self.subTest(text=text):
                self.assertTrue(checker.violations(text))

    def test_actual_teaching_content_is_allowed(self):
        text = """## Learning objectives
Compute softmax probabilities for the six candidate words.
Neural language models share parameters across similar words.
Lessons from this period set the stage for the AI resurgence.
For students using Windows, run the following command.
$$p_i = \\frac{e^{z_i}}{\\sum_j e^{z_j}}$$
"""
        self.assertEqual(checker.violations(text), [])

    def test_wrapped_match_reports_original_start_line(self):
        found = checker.violations("## Heading\n\nThis **sets**\nthe stage for neural models.")
        self.assertEqual(found[0][0], 3)


if __name__ == "__main__":
    unittest.main()
