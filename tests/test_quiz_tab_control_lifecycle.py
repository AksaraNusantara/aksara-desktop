"""
Tests for QuizTab control lifecycle transitions.
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
        self.calls.append(difficulty)

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


class TestQuizTabControlLifecycle(unittest.TestCase):
    """Test Quiz control transitions."""

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

    def _enter_feedback(self):
        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

    def test_idle_state_allows_start(self):
        """Idle state allows starting a Quiz."""

        self.assertTrue(
            self.quiz_tab.start_enabled,
        )

        self.assertFalse(
            self.quiz_tab.cancel_enabled,
        )

    def test_active_state_allows_cancel(self):
        """Active Quiz allows cancellation."""

        self._start_quiz()

        self.assertTrue(
            self.quiz_tab.cancel_enabled,
        )

    def test_active_state_requires_answer_before_check(self):
        """Check is unavailable before selecting an answer."""

        self._start_quiz()

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_answer_selection_enables_check(self):
        """Selecting an answer enables Check."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")

        self.assertTrue(
            self.quiz_tab.check_enabled,
        )

    def test_feedback_disables_check(self):
        """Feedback disables Check."""

        self._enter_feedback()

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_feedback_enables_next(self):
        """Feedback enables Next."""

        self._enter_feedback()

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

    def test_next_question_closes_feedback(self):
        """Next question clears the feedback state."""

        self._enter_feedback()

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

    def test_next_question_requires_feedback(self):
        """Next cannot be used before feedback."""

        self._start_quiz()

        with self.assertRaises(RuntimeError):
            self.quiz_tab.next_question()

    def test_cancel_restores_idle_controls(self):
        """Cancel restores the idle control state."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

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

    def test_completion_restores_idle_controls(self):
        """Completion restores the idle control state."""

        self._enter_feedback()

        self.quiz_tab.next_question()

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


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )
