"""
Tests for QuizTab difficulty interaction guards.
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


class TestQuizTabDifficultyGuard(unittest.TestCase):
    """Test Quiz difficulty interaction boundaries."""

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

    def test_difficulty_is_enabled_before_quiz(self):
        """Difficulty can be changed while Quiz is idle."""

        self.assertTrue(
            self.quiz_tab.difficulty_enabled,
        )

    def test_difficulty_is_disabled_during_quiz(self):
        """Difficulty is locked during an active Quiz."""

        self._start_quiz()

        self.assertFalse(
            self.quiz_tab.difficulty_enabled,
        )

    def test_difficulty_remains_disabled_during_feedback(self):
        """Difficulty remains locked during feedback."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertFalse(
            self.quiz_tab.difficulty_enabled,
        )

    def test_difficulty_is_enabled_after_completion(self):
        """Difficulty becomes editable after completion."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.difficulty_enabled,
        )

    def test_difficulty_is_enabled_after_cancel(self):
        """Difficulty becomes editable after cancellation."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.difficulty_enabled,
        )

    def test_active_quiz_keeps_original_difficulty(self):
        """Active Quiz retains its original difficulty."""

        self._start_quiz()

        self.assertEqual(
            self.generator.calls[-1],
            QuizDifficulty.LEVEL_1,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )