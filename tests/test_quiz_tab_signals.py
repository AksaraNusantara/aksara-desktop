"""
Tests for QuizTab lifecycle signals.
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


class TestQuizTabSignals(unittest.TestCase):
    """Test QuizTab lifecycle signal behavior."""

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

        self.started_count = 0
        self.cancelled_count = 0
        self.completed_count = 0

        self.quiz_tab.quiz_started.connect(
            self._on_quiz_started,
        )

        self.quiz_tab.quiz_cancelled.connect(
            self._on_quiz_cancelled,
        )

        self.quiz_tab.quiz_completed.connect(
            self._on_quiz_completed,
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def _on_quiz_started(self):
        self.started_count += 1

    def _on_quiz_cancelled(self):
        self.cancelled_count += 1

    def _on_quiz_completed(self):
        self.completed_count += 1

    def _start_quiz(self):
        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

    def _complete_quiz(self):
        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

    def test_start_emits_started_once(self):
        """Starting a Quiz emits quiz_started exactly once."""

        self._start_quiz()

        self.assertEqual(
            self.started_count,
            1,
        )

    def test_start_does_not_emit_cancelled(self):
        """Starting a Quiz does not emit quiz_cancelled."""

        self._start_quiz()

        self.assertEqual(
            self.cancelled_count,
            0,
        )

    def test_start_does_not_emit_completed(self):
        """Starting a Quiz does not emit quiz_completed."""

        self._start_quiz()

        self.assertEqual(
            self.completed_count,
            0,
        )

    def test_cancel_emits_cancelled_once(self):
        """Cancelling a Quiz emits quiz_cancelled exactly once."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        self.assertEqual(
            self.cancelled_count,
            1,
        )

    def test_cancel_does_not_emit_completed(self):
        """Cancelling a Quiz does not emit quiz_completed."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        self.assertEqual(
            self.completed_count,
            0,
        )

    def test_cancel_does_not_emit_started(self):
        """Cancelling a Quiz does not emit quiz_started."""

        self._start_quiz()

        self.quiz_tab.cancel_quiz()

        self.assertEqual(
            self.started_count,
            1,
        )

    def test_completion_emits_completed_once(self):
        """Completing a Quiz emits quiz_completed exactly once."""

        self._complete_quiz()

        self.assertEqual(
            self.completed_count,
            1,
        )

    def test_completion_does_not_emit_cancelled(self):
        """Completing a Quiz does not emit quiz_cancelled."""

        self._complete_quiz()

        self.assertEqual(
            self.cancelled_count,
            0,
        )

    def test_completion_does_not_emit_extra_started(self):
        """Completing a Quiz does not emit another quiz_started."""

        self._complete_quiz()

        self.assertEqual(
            self.started_count,
            1,
        )

    def test_next_question_does_not_emit_lifecycle_signals(self):
        """Moving to the next question emits no lifecycle signal."""

        self._start_quiz()

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        started_before = self.started_count
        cancelled_before = self.cancelled_count
        completed_before = self.completed_count

        self.quiz_tab.next_question()

        self.assertEqual(
            self.started_count,
            started_before,
        )

        self.assertEqual(
            self.cancelled_count,
            cancelled_before,
        )

        self.assertEqual(
            self.completed_count,
            completed_before + 1,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )