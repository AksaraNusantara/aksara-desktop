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
from application.learning.quiz.quiz_difficulty import QuizDifficulty


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
            difficulty=QuizDifficulty.LEVEL_1,
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
            difficulty=QuizDifficulty.LEVEL_1,
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
            difficulty=QuizDifficulty.LEVEL_3,
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
            difficulty=QuizDifficulty.LEVEL_1,
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

    def test_difficulty_cannot_exceed_available_data(self):
        """Difficulty cannot require more characters than available."""

        generator = QuizGenerator(
            self.characters[:3],
        )

        with self.assertRaises(ValueError):
            generator.generate(
                difficulty=QuizDifficulty.LEVEL_4,
            )

    def test_level_1_generates_one_character(self):
        """Level 1 generates a one-character question."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            difficulty=QuizDifficulty.LEVEL_1,
        )

        self.assertEqual(
            len(question.prompt.split()),
            1,
        )


    def test_level_2_generates_two_characters(self):
        """Level 2 generates a two-character question."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            difficulty=QuizDifficulty.LEVEL_2,
        )

        self.assertEqual(
            len(question.prompt.split()),
            2,
        )


    def test_level_3_generates_three_characters(self):
        """Level 3 generates a three-character question."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            difficulty=QuizDifficulty.LEVEL_3,
        )

        self.assertEqual(
            len(question.prompt.split()),
            3,
        )


    def test_level_4_generates_four_characters(self):
        """Level 4 generates a four-character question."""

        generator = QuizGenerator(
            self.characters,
        )

        question = generator.generate(
            difficulty=QuizDifficulty.LEVEL_4,
        )

        self.assertEqual(
            len(question.prompt.split()),
            4,
        )


    def test_invalid_difficulty_is_rejected(self):
        """Generator rejects an invalid difficulty value."""

        generator = QuizGenerator(
            self.characters,
        )

        with self.assertRaises(ValueError):
            generator.generate(
                difficulty=99,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)