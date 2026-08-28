"""Tests for the AD-QT-01 Quiz completion contract."""

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
    def __init__(self):
        self.calls = []
        self.question = SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=("ha", "na", "ca", "ra"),
        )

    def generate(self, difficulty):
        self.calls.append(difficulty)
        return self.question


class FakeLearningService:
    def __init__(self):
        self.calls = []

    def record_quiz_result(self, learner_id, result, timestamp=None):
        self.calls.append({
            "learner_id": learner_id,
            "result": result,
            "timestamp": timestamp,
        })


class TestQuizTabCompletion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.generator = FakeQuizGenerator()
        self.learning_service = FakeLearningService()
        self.quiz_tab = QuizTab(
            generator=self.generator,
            learning_service=self.learning_service,
            learner_id="test-learner",
        )
        self.completed_count = 0
        self.finished_count = 0
        self.quiz_tab.quiz_completed.connect(
            lambda: setattr(
                self, "completed_count", self.completed_count + 1
            )
        )
        self.quiz_tab.quiz_finished.connect(
            lambda: setattr(
                self, "finished_count", self.finished_count + 1
            )
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

    def _complete_quiz(self):
        self.quiz_tab.start_quiz(QuizDifficulty.LEVEL_1, 1)
        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")
        self.quiz_tab.next_question()

    def test_final_answer_disables_next_and_shows_result(self):
        self._complete_quiz()
        self.assertFalse(self.quiz_tab.next_enabled)
        self.assertTrue(self.quiz_tab.is_result_visible)
        self.assertFalse(self.quiz_tab.is_quiz_active)

    def test_completed_quiz_persists_result_once(self):
        self._complete_quiz()
        self.assertEqual(len(self.learning_service.calls), 1)
        self.assertEqual(
            self.learning_service.calls[0]["learner_id"],
            "test-learner",
        )
        self.assertEqual(self.completed_count, 1)

    def test_result_view_exposes_retry_and_finish(self):
        self._complete_quiz()
        self.assertTrue(self.quiz_tab.is_result_visible)
        self.assertTrue(self.quiz_tab.retry_button.isEnabled())
        self.assertTrue(self.quiz_tab.finish_button.isEnabled())

    def test_retry_starts_new_quiz_without_second_persistence(self):
        self._complete_quiz()
        self.quiz_tab.retry_quiz()
        self.assertTrue(self.quiz_tab.is_quiz_active)
        self.assertFalse(self.quiz_tab.is_result_visible)
        self.assertEqual(len(self.learning_service.calls), 1)
        self.assertEqual(self.quiz_tab.progress_text, "Soal 1 dari 1")

    def test_finish_returns_to_ready(self):
        self._complete_quiz()
        self.quiz_tab.finish_quiz()
        self.assertFalse(self.quiz_tab.is_quiz_active)
        self.assertFalse(self.quiz_tab.is_result_visible)
        self.assertTrue(self.quiz_tab.start_enabled)
        self.assertFalse(self.quiz_tab.cancel_enabled)
        self.assertFalse(self.quiz_tab.next_enabled)
        self.assertEqual(self.finished_count, 1)

    def test_final_statistics_remain_visible_in_result(self):
        self._complete_quiz()
        self.assertEqual(self.quiz_tab.accuracy_text, "100%")
        self.assertEqual(self.quiz_tab.result_score_label.text(), "1 / 1")
        self.assertIn("Benar: 1", self.quiz_tab.result_statistics_label.text())
        self.assertIn("Salah: 0", self.quiz_tab.result_statistics_label.text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
