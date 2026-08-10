"""
Tests for QuizTab answer feedback contract.
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


class TestQuizTabFeedback(unittest.TestCase):
    """Test QuizTab answer feedback behavior."""

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

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def test_feedback_is_hidden_initially(self):
        """Feedback is hidden before an answer is checked."""

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

    def test_feedback_has_no_result_initially(self):
        """Feedback has no correctness result initially."""

        self.assertIsNone(
            self.quiz_tab.feedback_is_correct,
        )

    def test_feedback_text_is_empty_initially(self):
        """Feedback text is empty before checking."""

        self.assertEqual(
            self.quiz_tab.feedback_text,
            "",
        )

    def test_correct_answer_shows_positive_feedback(self):
        """Correct answer produces positive feedback."""

        self.quiz_tab.select_answer("ha")

        self.quiz_tab.submit_answer()

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertTrue(
            self.quiz_tab.feedback_is_correct,
        )

        self.assertTrue(
            self.quiz_tab.feedback_text,
        )

    def test_wrong_answer_shows_negative_feedback(self):
        """Wrong answer produces negative feedback."""

        self.quiz_tab.select_answer("na")

        self.quiz_tab.submit_answer()

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertFalse(
            self.quiz_tab.feedback_is_correct,
        )

        self.assertTrue(
            self.quiz_tab.feedback_text,
        )

    def test_wrong_answer_exposes_correct_answer(self):
        """Wrong answer exposes the correct answer."""

        self.quiz_tab.select_answer("na")

        self.quiz_tab.submit_answer()

        self.assertEqual(
            self.quiz_tab.correct_answer_text,
            "ha",
        )

    def test_correct_answer_does_not_expose_wrong_answer(self):
        """Correct feedback does not expose a correction."""

        self.quiz_tab.select_answer("ha")

        self.quiz_tab.submit_answer()

        self.assertEqual(
            self.quiz_tab.correct_answer_text,
            "",
        )

    def test_feedback_resets_for_next_question(self):
        """Generating the next question clears previous feedback."""

        self.quiz_tab.select_answer("ha")

        self.quiz_tab.submit_answer()

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

        self.assertIsNone(
            self.quiz_tab.feedback_is_correct,
        )

        self.assertEqual(
            self.quiz_tab.feedback_text,
            "",
        )

        self.assertEqual(
            self.quiz_tab.correct_answer_text,
            "",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )