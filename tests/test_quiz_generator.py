"""
Tests for QuizGenerator.

QuizGenerator operates on character records supplied by the active
ScriptPack and has no dependency on a specific writing system.
"""

from pathlib import Path
import sys
import unittest


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.learning.quiz.quiz_generator import QuizGenerator
from application.learning.quiz.quiz_question import QuizQuestion


class TestQuizGenerator(unittest.TestCase):
    """Test QuizGenerator."""

    def setUp(self) -> None:
        """Create sample ScriptPack character data."""

        self.characters = [
            {
                "glyph": "ꦲ",
                "latin": "ha",
                "description": "Ha",
            },
            {
                "glyph": "ꦤ",
                "latin": "na",
                "description": "Na",
            },
            {
                "glyph": "ꦕ",
                "latin": "ca",
                "description": "Ca",
            },
            {
                "glyph": "ꦫ",
                "latin": "ra",
                "description": "Ra",
            },
            {
                "glyph": "ꦏ",
                "latin": "ka",
                "description": "Ka",
            },
        ]

    def test_generate_question(self):
        """Generator creates a valid QuizQuestion."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            character_count=1,
        )

        self.assertIsInstance(
            question,
            QuizQuestion,
        )

        self.assertTrue(
            question.prompt,
        )

        self.assertTrue(
            question.correct_answer,
        )

        self.assertEqual(
            len(question.options),
            4,
        )

    def test_correct_answer_is_in_options(self):
        """Generated correct answer is always available."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            character_count=1,
        )

        self.assertIn(
            question.correct_answer,
            question.options,
        )

    def test_multi_character_question(self):
        """Generator supports multi-character questions."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            character_count=3,
        )

        self.assertEqual(
            len(question.prompt.split()),
            3,
        )

        self.assertEqual(
            len(question.correct_answer.split()),
            3,
        )

    def test_custom_option_count(self):
        """Generator supports a custom option count."""

        generator = QuizGenerator(
            self.characters,
            option_count=3,
        )

        question = generator.generate(
            character_count=1,
        )

        self.assertEqual(
            len(question.options),
            3,
        )

    def test_empty_characters_are_rejected(self):
        """Generator requires character data."""

        with self.assertRaises(ValueError):
            QuizGenerator([])

    def test_invalid_option_count_is_rejected(self):
        """At least two answer options are required."""

        with self.assertRaises(ValueError):
            QuizGenerator(
                self.characters,
                option_count=1,
            )

    def test_invalid_character_count_is_rejected(self):
        """Character count must be positive."""

        generator = QuizGenerator(
            self.characters,
        )

        with self.assertRaises(ValueError):
            generator.generate(
                character_count=0,
            )

    def test_character_count_cannot_exceed_available_data(self):
        """Question cannot contain more characters than available."""

        generator = QuizGenerator(
            self.characters,
        )

        with self.assertRaises(ValueError):
            generator.generate(
                character_count=10,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)