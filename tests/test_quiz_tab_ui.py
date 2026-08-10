"""
Tests for QuizTab UI state contract.
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
from application.learning.quiz.quiz_session import QuizSessionState

from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Minimal QuizGenerator test double."""

    def __init__(self):
        self.calls = []

    def generate(self, difficulty):
        self.calls.append(difficulty)

        return SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=(
                "ha",
                "na",
                "ca",
                "ra",
            ),
        )


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


class TestQuizTabUIState(unittest.TestCase):
    """Test QuizTab UI state behavior."""

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

    def test_initial_ui_state(self):
        """QuizTab starts in the idle UI state."""

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

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

    def test_start_changes_ui_state(self):
        """Starting Quiz changes the UI to active state."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertFalse(
            self.quiz_tab.difficulty_enabled,
        )

        self.assertFalse(
            self.quiz_tab.start_enabled,
        )

        self.assertTrue(
            self.quiz_tab.cancel_enabled,
        )

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_difficulty_disabled_during_quiz(self):
        """Difficulty cannot be changed during an active Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_3,
            total_questions=2,
        )

        self.assertFalse(
            self.quiz_tab.difficulty_enabled,
        )

    def test_cancel_enabled_during_quiz(self):
        """Cancel is enabled during an active Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertTrue(
            self.quiz_tab.cancel_enabled,
        )

    def test_check_disabled_without_answer(self):
        """Check remains disabled until an answer is selected."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_check_enabled_after_answer_selection(self):
        """Selecting an answer enables Check."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer(
            "ha",
        )

        self.assertTrue(
            self.quiz_tab.check_enabled,
        )

    def test_next_question_resets_answer_selection(self):
        """Next question clears the selected answer state."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer(
            "ha",
        )

        self.assertTrue(
            self.quiz_tab.check_enabled,
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.assertTrue(
            self.is_active_session(),
        )

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_completed_quiz_restores_idle_state(self):
        """Completing Quiz restores the idle UI state."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer(
            "ha",
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

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

    def test_cancelled_quiz_restores_idle_state(self):
        """Cancelling Quiz restores the idle UI state."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

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

    def is_active_session(self):
        """Return whether QuizSession remains active."""

        session = self.quiz_tab.session

        return (
            session is not None
            and session.state is QuizSessionState.ACTIVE
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )