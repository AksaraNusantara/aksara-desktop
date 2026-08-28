"""
Tests for the QuizTab feedback-to-next-question flow.
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


class TestQuizTabNextQuestion(unittest.TestCase):
    """Test the feedback-to-next-question flow."""

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

    def test_next_button_is_present(self):
        """Next button is part of the feedback flow."""

        self.assertIsNotNone(
            self.quiz_tab.next_button,
        )

    def test_next_is_disabled_before_feedback(self):
        """Next remains disabled before an answer is checked."""

        self.assertFalse(
            self.quiz_tab.next_enabled,
        )

    def test_submit_shows_feedback_without_generating_next_question(self):
        """Submitting an answer shows feedback but does not advance."""

        initial_call_count = len(
            self.generator.calls,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.assertEqual(
            len(self.generator.calls),
            initial_call_count,
        )

        self.assertEqual(
            self.quiz_tab.question_label.text(),
            "ꦲ",
        )

    def test_next_generates_next_question(self):
        """Next generates the following question."""

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.quiz_tab.next_question()

        self.assertEqual(
            len(self.generator.calls),
            2,
        )

        self.assertEqual(
            self.quiz_tab.question_label.text(),
            "ꦤ",
        )

    def test_next_clears_feedback(self):
        """Next clears feedback state."""

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

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

    def test_next_clears_answer_selection(self):
        """Next clears the selected answer."""

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.quiz_tab.next_question()

        self.assertIsNone(
            self.quiz_tab.selected_answer,
        )

    def test_next_disables_check(self):
        """Check is disabled for the new question."""

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

    def test_next_disables_itself_after_advancing(self):
        """Next is disabled until another answer is checked."""

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.next_enabled,
        )

    def test_final_answer_completes_quiz(self):
        """The final answer completes the Quiz and shows the Result view."""

        # Question 1
        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.assertTrue(
            self.quiz_tab.next_enabled,
        )

        # Question 2 — final question
        self.quiz_tab.next_question()
        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer()

        # Final answer → RESULT
        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertTrue(
            self.quiz_tab.is_result_visible,
        )

        self.assertFalse(
            self.quiz_tab.next_enabled,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )