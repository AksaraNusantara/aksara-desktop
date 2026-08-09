"""
Tests for the static QuizTab visual skeleton.
"""

from pathlib import Path
import sys
import unittest
from types import SimpleNamespace


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from PySide6.QtWidgets import QApplication

from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Minimal QuizGenerator test double."""

    def generate(self, difficulty):
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

    def record_quiz_result(
        self,
        learner_id,
        result,
        timestamp=None,
    ):
        pass


class TestQuizTabVisualSkeleton(unittest.TestCase):
    """Verify the presence of the QuizTab visual regions."""

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

    def test_title_is_present(self):
        """Quiz title is present."""

        self.assertIsNotNone(
            self.quiz_tab.title_label,
        )

        self.assertTrue(
            self.quiz_tab.title_label.text(),
        )

    def test_difficulty_selector_is_present(self):
        """Difficulty selector is present."""

        self.assertIsNotNone(
            self.quiz_tab.difficulty_combo,
        )

    def test_progress_label_is_present(self):
        """Question progress display is present."""

        self.assertIsNotNone(
            self.quiz_tab.progress_label,
        )

    def test_question_label_is_present(self):
        """Question display is present."""

        self.assertIsNotNone(
            self.quiz_tab.question_label,
        )

    def test_instruction_label_is_present(self):
        """Question instruction is present."""

        self.assertIsNotNone(
            self.quiz_tab.instruction_label,
        )

    def test_answer_buttons_are_present(self):
        """Four answer controls are present."""

        self.assertEqual(
            len(self.quiz_tab.answer_buttons),
            4,
        )

    def test_check_button_is_present(self):
        """Check button is present."""

        self.assertIsNotNone(
            self.quiz_tab.check_button,
        )

    def test_cancel_button_is_present(self):
        """Cancel button is present."""

        self.assertIsNotNone(
            self.quiz_tab.cancel_button,
        )

    def test_statistics_are_present(self):
        """Quiz statistics displays are present."""

        self.assertIsNotNone(
            self.quiz_tab.correct_label,
        )

        self.assertIsNotNone(
            self.quiz_tab.incorrect_label,
        )

        self.assertIsNotNone(
            self.quiz_tab.accuracy_label,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )