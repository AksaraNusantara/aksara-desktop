"""
Tests for QuizTab statistics visual binding.
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


class TestQuizTabStatisticsUI(unittest.TestCase):
    """Test visual binding of Quiz statistics."""

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

    def test_statistics_labels_are_zero_initially(self):
        """Statistics labels show zero before Quiz."""

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 0",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 0%",
        )

    def test_statistics_labels_update_after_correct_answer(self):
        """Statistics labels update after a correct answer."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 1",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 100%",
        )

    def test_statistics_labels_update_after_incorrect_answer(self):
        """Statistics labels update after an incorrect answer."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer("na")

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 0",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 1",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 0%",
        )

    def test_statistics_labels_update_during_feedback(self):
        """Statistics labels reflect the current feedback result."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 1",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 100%",
        )

    def test_statistics_labels_persist_after_next_question(self):
        """Statistics labels persist after advancing."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 1",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 100%",
        )

    def test_statistics_labels_remain_visible_in_result(self):
        """Final statistics remain available while Result is displayed."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 1",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 100%",
        )

    def test_statistics_labels_reset_after_cancel(self):
        """Statistics labels return to zero after cancellation."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.correct_label.text(),
            "Benar: 0",
        )

        self.assertEqual(
            self.quiz_tab.incorrect_label.text(),
            "Salah: 0",
        )

        self.assertEqual(
            self.quiz_tab.accuracy_label.text(),
            "Akurasi: 0%",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )