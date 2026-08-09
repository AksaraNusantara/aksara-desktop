"""
Tests for QuizDifficulty.
"""

from pathlib import Path
import sys
import unittest


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.learning.quiz.quiz_difficulty import QuizDifficulty


class TestQuizDifficulty(unittest.TestCase):
    """Test Quiz difficulty definitions."""

    def test_level_1_uses_one_character(self):
        """Level 1 represents one character."""

        self.assertEqual(
            QuizDifficulty.LEVEL_1.character_count,
            1,
        )

    def test_level_2_uses_two_characters(self):
        """Level 2 represents two characters."""

        self.assertEqual(
            QuizDifficulty.LEVEL_2.character_count,
            2,
        )

    def test_level_3_uses_three_characters(self):
        """Level 3 represents three characters."""

        self.assertEqual(
            QuizDifficulty.LEVEL_3.character_count,
            3,
        )

    def test_level_4_uses_four_characters(self):
        """Level 4 represents four characters."""

        self.assertEqual(
            QuizDifficulty.LEVEL_4.character_count,
            4,
        )

    def test_all_levels_are_distinct(self):
        """Every difficulty level has a unique value."""

        values = {
            difficulty.value
            for difficulty in QuizDifficulty
        }

        self.assertEqual(
            len(values),
            4,
        )

    def test_difficulty_is_an_enum(self):
        """QuizDifficulty is an Enum."""

        self.assertTrue(
            issubclass(
                QuizDifficulty,
                __import__("enum").Enum,
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)