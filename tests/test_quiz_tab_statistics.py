"""
Tests for QuizTab statistics state.
"""

from pathlib import Path
import sys
import unittest
from types import SimpleNamespace


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from PySide6.QtWidgets import QApplication

from application.learning.quiz.quiz_difficulty import QuizDifficulty

from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Deterministic QuizGenerator test double."""

    def __init__(self):
        self.calls = []

        self.questions = [
            SimpleNamespace(
                prompt="ꦲ",
                correct_answer="ha",
                options=(
                    "ha",
                    "na",
                    "ca",
                    "ra",
                ),
            ),
            SimpleNamespace(
                prompt="ꦤ",
                correct_answer="na",
                options=(
                    "na",
                    "ca",
                    "ra",
                    "ka",
                ),
            ),
            SimpleNamespace(
                prompt="ꦕ",
                correct_answer="ca",
                options=(
                    "ca",
                    "ra",
                    "ka",
                    "da",
                ),
            ),
        ]

    def generate(self, difficulty):
        self.calls.append(difficulty)

        index = min(
            len(self.calls) - 1,
            len(self.questions) - 1,
        )

        return self.questions[index]


class FakeLearningService:
    """Minimal LearningService test double."""

    def __init__(self):
        self.calls = []

    def record_quiz_result(
        self,
        learner_id,
        result,
        timestamp=None,
    ):
        self.calls.append(
            {
                "learner_id": learner_id,
                "result": result,
                "timestamp": timestamp,
            }
        )


class TestQuizTabStatistics(unittest.TestCase):
    """Test QuizTab statistics state."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()

        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        self.generator = FakeQuizGenerator()
        self.learning_service = FakeLearningService()

        self.quiz_tab = QuizTab(
            generator=self.generator,
            learning_service=self.learning_service,
            learner_id="test-learner",
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def test_statistics_are_zero_before_quiz(self):
        """Statistics start at zero before a Quiz."""

        self.assertEqual(
            self.quiz_tab.correct_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )

    def test_correct_answer_updates_statistics(self):
        """A correct answer increments correct count."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "100%",
        )

    def test_incorrect_answer_updates_statistics(self):
        """An incorrect answer increments incorrect count."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("na")
        self.quiz_tab.submit_answer("na")

        self.assertEqual(
            self.quiz_tab.correct_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )

    def test_mixed_answers_update_statistics(self):
        """Correct and incorrect answers produce aggregate statistics."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.quiz_tab.select_answer("ca")
        self.quiz_tab.submit_answer("ca")

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "50%",
        )

    def test_statistics_update_during_feedback(self):
        """Statistics reflect the submitted answer during feedback."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "100%",
        )

    def test_statistics_persist_across_next_question(self):
        """Statistics remain accumulated after advancing."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "100%",
        )

    def test_statistics_reset_after_completion(self):
        """Statistics reset after Quiz completion."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.correct_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )

    def test_statistics_reset_after_cancel(self):
        """Cancelled Quiz resets statistics."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.correct_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )