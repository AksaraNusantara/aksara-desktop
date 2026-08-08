"""
Tests for QuizQuestion.

QuizQuestion represents one generated question and is temporary
Quiz application state.
"""

from pathlib import Path
import sys
import unittest


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.learning.quiz.quiz_question import QuizQuestion


class TestQuizQuestion(unittest.TestCase):
    """Test QuizQuestion validation and immutability."""

    def test_valid_question(self):
        """A valid question can be created."""

        question = QuizQuestion(
            prompt="ꦲ",
            correct_answer="ha",
            options=(
                "ha",
                "na",
                "ca",
                "ra",
            ),
        )

        self.assertEqual(
            question.prompt,
            "ꦲ",
        )

        self.assertEqual(
            question.correct_answer,
            "ha",
        )

        self.assertEqual(
            len(question.options),
            4,
        )

    def test_empty_prompt_is_rejected(self):
        """Prompt cannot be empty."""

        with self.assertRaises(ValueError):
            QuizQuestion(
                prompt="",
                correct_answer="ha",
                options=("ha", "na"),
            )

    def test_empty_correct_answer_is_rejected(self):
        """Correct answer cannot be empty."""

        with self.assertRaises(ValueError):
            QuizQuestion(
                prompt="ꦲ",
                correct_answer="",
                options=("ha", "na"),
            )

    def test_empty_options_are_rejected(self):
        """Question must contain answer options."""

        with self.assertRaises(ValueError):
            QuizQuestion(
                prompt="ꦲ",
                correct_answer="ha",
                options=(),
            )

    def test_correct_answer_must_exist_in_options(self):
        """Correct answer must be one of the available options."""

        with self.assertRaises(ValueError):
            QuizQuestion(
                prompt="ꦲ",
                correct_answer="ha",
                options=("na", "ca"),
            )

    def test_duplicate_options_are_rejected(self):
        """Answer options must be unique."""

        with self.assertRaises(ValueError):
            QuizQuestion(
                prompt="ꦲ",
                correct_answer="ha",
                options=(
                    "ha",
                    "ha",
                    "na",
                ),
            )

    def test_question_is_immutable(self):
        """QuizQuestion cannot be modified after creation."""

        question = QuizQuestion(
            prompt="ꦲ",
            correct_answer="ha",
            options=("ha", "na"),
        )

        with self.assertRaises(AttributeError):
            question.prompt = "ꦤ"


if __name__ == "__main__":
    unittest.main(verbosity=2)