"""
Tests for QuizTab answer button UI state.
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

    def record_quiz_result(
        self,
        learner_id,
        result,
        timestamp=None,
    ):
        pass


class TestQuizTabAnswerButtonsUI(unittest.TestCase):
    """Test answer button enabled state across Quiz lifecycle."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()

        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        self.quiz_tab = QuizTab(
            generator=FakeQuizGenerator(),
            learning_service=FakeLearningService(),
            learner_id="test-learner",
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def _answer_button_states(self):
        return [
            button.isEnabled()
            for button in self.quiz_tab.answer_buttons
        ]

    def _start_quiz(self):
        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

    def test_answer_buttons_are_disabled_before_quiz(self):
        """Answer buttons are disabled while Quiz is idle."""

        self.assertEqual(
            self._answer_button_states(),
            [False, False, False, False],
        )

    def test_answer_buttons_are_enabled_during_question(self):
        """Answer buttons are enabled during an active question."""

        self._start_quiz()

        self.assertEqual(
            self._answer_button_states(),
            [True, True, True, True],
        )

    def test_answer_buttons_are_disabled_during_feedback(self):
        """Answer buttons are disabled while feedback is visible."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertEqual(
            self._answer_button_states(),
            [False, False, False, False],
        )

    def test_answer_buttons_are_enabled_on_next_question(self):
        """Answer buttons are re-enabled for the next question."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

        self.assertEqual(
            self._answer_button_states(),
            [True, True, True, True],
        )

    def test_answer_buttons_are_disabled_after_completion(self):
        """Answer buttons are disabled after Quiz completion."""

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

        self.assertEqual(
            self._answer_button_states(),
            [False, False, False, False],
        )

    def test_answer_buttons_are_disabled_after_cancel(self):
        """Answer buttons are disabled after Quiz cancellation."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self._answer_button_states(),
            [False, False, False, False],
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )