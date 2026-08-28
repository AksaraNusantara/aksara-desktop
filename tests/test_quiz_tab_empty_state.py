"""Tests for the QuizTab no-active-ScriptPack state."""

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
    def generate(self, difficulty):
        return SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=("ha", "na", "ca", "ra"),
        )


class FakeLearningService:
    def record_quiz_result(self, learner_id, result, timestamp=None):
        pass


class TestQuizTabEmptyState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.scriptpack_active = False
        self.quiz_tab = QuizTab(
            generator=FakeQuizGenerator(),
            learning_service=FakeLearningService(),
            learner_id="test-learner",
            scriptpack_active=lambda: self.scriptpack_active,
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def test_no_active_scriptpack_shows_empty_state(self):
        self.assertIs(
            self.quiz_tab._view_stack.currentWidget(),
            self.quiz_tab._empty_state,
        )
        self.assertFalse(self.quiz_tab.start_button.isEnabled())
        self.assertFalse(self.quiz_tab.difficulty_combo.isEnabled())
        self.assertEqual(
            self.quiz_tab._empty_state.title_label.text(),
            "No ScriptPack Activated",
        )

    def test_open_home_action_is_forwarded(self):
        requested = []
        self.quiz_tab.open_home_requested.connect(
            lambda: requested.append(True),
        )

        self.quiz_tab._empty_state.action_button.click()

        self.assertEqual(requested, [True])

    def test_activation_restores_quiz_ready_view(self):
        self.scriptpack_active = True
        self.quiz_tab.refresh()

        self.assertIs(
            self.quiz_tab._view_stack.currentWidget(),
            self.quiz_tab.quiz_content_widget,
        )
        self.assertTrue(self.quiz_tab.start_button.isEnabled())
        self.assertTrue(self.quiz_tab.difficulty_combo.isEnabled())


if __name__ == "__main__":
    unittest.main(verbosity=2)
