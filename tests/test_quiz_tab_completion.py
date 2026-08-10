"""
Tests for QuizTab completion contract.
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
        ]

    def generate(self, difficulty):
        self.calls.append(difficulty)

        return self.questions[0]


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


class TestQuizTabCompletion(unittest.TestCase):
    """Test QuizTab completion behavior."""

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

    def _complete_quiz(self):
        """Complete the one-question Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.quiz_tab.next_question()

    def test_completed_quiz_is_not_active(self):
        """Completed Quiz is no longer active."""

        self._complete_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

    def test_completed_quiz_emits_completion(self):
        """Completed Quiz emits quiz_completed once."""

        self._complete_quiz()

        self.assertEqual(
            self.completed_count,
            1,
        )

    def test_completed_quiz_persists_result_once(self):
        """Completed Quiz persists exactly one result."""

        self._complete_quiz()

        self.assertEqual(
            len(self.learning_service.calls),
            1,
        )

    def test_completed_quiz_restores_idle_controls(self):
        """Completed Quiz restores idle controls."""

        self._complete_quiz()

        self.assertTrue(
            self.quiz_tab.difficulty_enabled,
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

    def test_completed_quiz_resets_progress(self):
        """Completed Quiz resets progress."""

        self._complete_quiz()

        self.assertEqual(
            self.quiz_tab.progress_text,
            "—",
        )

    def test_completed_quiz_resets_statistics(self):
        """Completed Quiz resets statistics."""

        self._complete_quiz()

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

    def test_completed_quiz_cannot_submit_again(self):
        """Completed Quiz cannot accept another answer."""

        self._complete_quiz()

        with self.assertRaises(RuntimeError):
            self.quiz_tab.submit_answer("ha")

    def test_completed_quiz_cannot_complete_again(self):
        """Completed Quiz cannot emit completion again."""

        self._complete_quiz()

        with self.assertRaises(RuntimeError):
            self.quiz_tab.next_question()

        self.assertEqual(
            self.completed_count,
            1,
        )

        self.assertEqual(
            len(self.learning_service.calls),
            1,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )