"""
Tests for the QuizTab application/UI boundary.

These tests focus on Quiz lifecycle coordination.
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


class TestQuizTab(unittest.TestCase):
    """Test QuizTab lifecycle coordination."""

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

    def test_initial_state_is_idle(self):
        """QuizTab starts without an active session."""

        self.assertIsNone(
            self.quiz_tab.session,
        )

    def test_start_creates_active_session(self):
        """Starting Quiz creates an active QuizSession."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertIsNotNone(
            self.quiz_tab.session,
        )

        self.assertIs(
            self.quiz_tab.session.state,
            QuizSessionState.ACTIVE,
        )

    def test_start_uses_selected_difficulty(self):
        """QuizTab passes difficulty to QuizGenerator."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_3,
            total_questions=1,
        )

        self.assertEqual(
            self.generator.calls,
            [
                QuizDifficulty.LEVEL_3,
            ],
        )

    def test_start_emits_quiz_started(self):
        """Starting Quiz emits quiz_started."""

        calls = []

        self.quiz_tab.quiz_started.connect(
            lambda: calls.append(True),
        )

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertEqual(
            calls,
            [True],
        )

    def test_cancel_emits_quiz_cancelled(self):
        """Cancelling an active Quiz emits quiz_cancelled."""

        calls = []

        self.quiz_tab.quiz_cancelled.connect(
            lambda: calls.append(True),
        )

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.cancel_quiz()

        self.assertEqual(
            calls,
            [True],
        )

        self.assertIsNone(
            self.quiz_tab.session,
        )

    def test_cancel_does_not_persist_result(self):
        """Cancelled Quiz does not call LearningService."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.cancel_quiz()

        self.assertEqual(
            self.learning_service.calls,
            [],
        )

    def test_completed_quiz_persists_result(self):
        """Completed Quiz sends QuizResult to LearningService."""

        calls = []

        self.quiz_tab.quiz_completed.connect(
            lambda: calls.append(True),
        )

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.assertEqual(
            len(self.learning_service.calls),
            0,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertEqual(
            len(self.learning_service.calls),
            1,
        )

        self.assertEqual(
            self.learning_service.calls[0]["learner_id"],
            "test-learner",
        )

        self.assertEqual(
            calls,
            [True],
        )

        self.assertIsNone(
            self.quiz_tab.session,
        )

    def test_answer_generates_next_question(self):
        """A non-final answer generates the next question."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.assertEqual(
            len(self.generator.calls),
            1,
        )

        self.quiz_tab.next_question()

        self.assertEqual(
            len(self.generator.calls),
            2,
        )

        self.assertIsNotNone(
            self.quiz_tab.session,
        )

        self.assertIs(
            self.quiz_tab.session.state,
            QuizSessionState.ACTIVE,
        )

    def test_next_question_uses_same_difficulty(self):
        """Every generated question uses the selected difficulty."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_3,
            total_questions=3,
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.quiz_tab.next_question()

        self.assertEqual(
            self.generator.calls,
            [
                QuizDifficulty.LEVEL_3,
                QuizDifficulty.LEVEL_3,
            ],
        )

    def test_quiz_remains_active_after_non_final_answer(self):
        """A non-final answer keeps the Quiz active."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.submit_answer("ha")

        self.assertIsNotNone(
            self.quiz_tab.session,
        )

        self.assertIs(
            self.quiz_tab.session.state,
            QuizSessionState.ACTIVE,
        )


    def test_final_answer_waits_for_next_to_complete(self):
        """Final answer waits for Next before completing the Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.submit_answer(
            "ha",
        )

        self.assertEqual(
            len(self.generator.calls),
            1,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertEqual(
            len(self.generator.calls),
            1,
        )

        self.assertIsNone(
            self.quiz_tab.session,
        )

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )