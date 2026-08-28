"""Tests for the AD-QT-01 QuizTab public contract."""

from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PySide6.QtWidgets import QApplication

from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Minimal deterministic QuizGenerator test double."""

    def generate(self, difficulty):
        return SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=("ha", "na", "ca", "ra"),
        )


class FakeLearningService:
    """Minimal LearningService test double."""

    def record_quiz_result(self, learner_id, result, timestamp=None):
        pass


class TestQuizTab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.quiz_tab = QuizTab(
            generator=FakeQuizGenerator(),
            learning_service=FakeLearningService(),
            learner_id="test-learner",
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def test_legacy_quiz_state_is_not_exposed(self):
        """QuizTab no longer exposes legacy state counters/session."""
        self.assertFalse(hasattr(self.quiz_tab, "correct_count"))
        self.assertFalse(hasattr(self.quiz_tab, "incorrect_count"))
        self.assertFalse(hasattr(self.quiz_tab, "session"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
