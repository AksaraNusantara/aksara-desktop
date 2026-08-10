"""
Tests for QuizTab answer interaction guards.
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
        self.question = SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=(
                "ha",
                "na",
                "ca",
                "ra",
            ),
        )

    def generate(self, difficulty):
        return self.question


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


class TestQuizTabAnswerGuard(unittest.TestCase):
    """Test answer interaction boundaries."""

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

    def _start_quiz(self):
        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

    def test_select_answer_requires_active_quiz(self):
        """Answer selection requires an active Quiz."""

        with self.assertRaises(RuntimeError):
            self.quiz_tab.select_answer("ha")

    def test_valid_answer_can_be_selected(self):
        """A valid answer can be selected during a Quiz."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")

        self.assertEqual(
            self.quiz_tab.selected_answer,
            "ha",
        )

    def test_invalid_answer_is_rejected(self):
        """An answer not present in options is rejected."""

        self._start_quiz()

        with self.assertRaises(ValueError):
            self.quiz_tab.select_answer("xx")

    def test_none_answer_is_rejected(self):
        """None cannot be selected as an answer."""

        self._start_quiz()

        with self.assertRaises(ValueError):
            self.quiz_tab.select_answer(None)

    def test_answer_cannot_change_after_submission(self):
        """Answer selection is closed during feedback."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        with self.assertRaises(RuntimeError):
            self.quiz_tab.select_answer("na")

    def test_answer_cannot_be_selected_after_completion(self):
        """Completed Quiz cannot accept answer selection."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        with self.assertRaises(RuntimeError):
            self.quiz_tab.select_answer("ha")

    def test_answer_cannot_be_selected_after_cancel(self):
        """Cancelled Quiz cannot accept answer selection."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        with self.assertRaises(RuntimeError):
            self.quiz_tab.select_answer("ha")

    def test_invalid_answer_does_not_mutate_selection(self):
        """Rejected answer does not replace the current selection."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")

        with self.assertRaises(ValueError):
            self.quiz_tab.select_answer("xx")

        self.assertEqual(
            self.quiz_tab.selected_answer,
            "ha",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )