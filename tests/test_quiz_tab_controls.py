"""
Tests for QuizTab interactive controls.
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


class TestQuizTabControls(unittest.TestCase):
    """Test QuizTab interactive controls."""

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

    def test_start_button_is_present(self):
        """Start button is present."""

        self.assertIsNotNone(
            self.quiz_tab.start_button,
        )

    def test_start_button_starts_quiz(self):
        """Clicking Start begins the Quiz."""

        self.quiz_tab.difficulty_combo.setCurrentIndex(1)

        self.quiz_tab.start_button.click()

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.generator.calls,
            [
                QuizDifficulty.LEVEL_2,
            ],
        )

    def test_start_uses_selected_difficulty(self):
        """Start maps the selected UI value to QuizDifficulty."""

        self.quiz_tab.difficulty_combo.setCurrentIndex(2)

        self.quiz_tab.start_button.click()

        self.assertEqual(
            self.generator.calls[-1],
            QuizDifficulty.LEVEL_3,
        )

    def test_start_disables_configuration_controls(self):
        """Starting Quiz disables difficulty and Start."""

        self.quiz_tab.start_button.click()

        self.assertFalse(
            self.quiz_tab.difficulty_enabled,
        )

        self.assertFalse(
            self.quiz_tab.start_enabled,
        )

    def test_answer_button_selects_answer(self):
        """Clicking an answer selects that answer."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.answer_buttons[0].click()

        self.assertTrue(
            self.quiz_tab.check_enabled,
        )

    def test_check_button_submits_selected_answer(self):
        """Check submits the selected answer."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.answer_buttons[0].click()

        self.quiz_tab.check_button.click()

        self.assertFalse(
            self.quiz_tab.check_enabled,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

    def test_cancel_button_cancels_quiz(self):
        """Cancel button cancels the active Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.cancel_button.click()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

    def test_answer_buttons_display_current_options(self):
        """Answer buttons display the current question options."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        options = (
            "ha",
            "na",
            "ca",
            "ra",
        )

        self.assertEqual(
            [
                button.text()
                for button in self.quiz_tab.answer_buttons
            ],
            list(options),
        )

    def test_question_display_updates_when_quiz_starts(self):
        """Starting Quiz displays the generated question."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertEqual(
            self.quiz_tab.question_label.text(),
            "ꦲ",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )