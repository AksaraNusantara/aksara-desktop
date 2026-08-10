"""
End-to-end integration tests for QuizTab lifecycle.
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


class TestQuizTabIntegration(unittest.TestCase):
    """Test the complete QuizTab lifecycle."""

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

        self.completed_count = 0

        self.quiz_tab.quiz_completed.connect(
            self._on_quiz_completed,
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def _on_quiz_completed(self):
        self.completed_count += 1

    def test_complete_quiz_lifecycle(self):
        """A complete Quiz lifecycle behaves consistently."""

        # -------------------------------------------------
        # START
        # -------------------------------------------------

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 2",
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

        # -------------------------------------------------
        # QUESTION 1 — CORRECT
        # -------------------------------------------------

        self.quiz_tab.select_answer("ha")

        self.assertTrue(
            self.quiz_tab.check_enabled,
        )

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

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 2",
        )

        # -------------------------------------------------
        # NEXT → QUESTION 2
        # -------------------------------------------------

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 2 dari 2",
        )

        self.assertEqual(
            self.quiz_tab.correct_count,
            1,
        )

        self.assertEqual(
            self.quiz_tab.incorrect_count,
            0,
        )

        # -------------------------------------------------
        # QUESTION 2 — INCORRECT
        # -------------------------------------------------

        self.quiz_tab.select_answer("ca")
        self.quiz_tab.submit_answer("ca")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

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

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 2 dari 2",
        )

        # -------------------------------------------------
        # COMPLETE
        # -------------------------------------------------

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.completed_count,
            1,
        )

        self.assertEqual(
            len(self.learning_service.calls),
            1,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "—",
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

        self.assertTrue(
            self.quiz_tab.start_enabled,
        )

        self.assertFalse(
            self.quiz_tab.cancel_enabled,
        )

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

        self.assertFalse(
            self.quiz_tab.next_enabled,
        )

    def test_new_quiz_after_completion_starts_clean(self):
        """A new Quiz starts with no state from the previous Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 2",
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

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

        self.assertIsNone(
            self.quiz_tab.selected_answer,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )