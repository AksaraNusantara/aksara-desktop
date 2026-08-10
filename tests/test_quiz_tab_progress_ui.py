"""
Tests for QuizTab progress visual binding.
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
            SimpleNamespace(
                prompt="ꦕ",
                correct_answer="ca",
                options=(
                    "ca",
                    "ra",
                    "ka",
                    "da",
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


class TestQuizTabProgressUI(unittest.TestCase):
    """Test visual binding of Quiz progress."""

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

    def test_progress_label_is_idle_initially(self):
        """Progress label shows idle state before Quiz."""
        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 0 / 0",
        )

    def test_progress_label_updates_when_quiz_starts(self):
        """Progress label shows the first question."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 1 dari 3",
        )

    def test_progress_label_remains_during_feedback(self):
        """Feedback does not change the visible progress."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 1 dari 3",
        )

    def test_progress_label_updates_after_next_question(self):
        """Progress label advances with the next question."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 2 dari 3",
        )

    def test_progress_label_updates_on_final_question(self):
        """Progress label shows the final question number."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        self.quiz_tab.select_answer("na")
        self.quiz_tab.submit_answer("na")
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 3 dari 3",
        )

    def test_progress_label_resets_after_completion(self):
        """Progress label returns to idle after Quiz completion."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 1 dari 1",
        )

        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "—",
        )

    def test_progress_label_resets_after_cancel(self):
        """Progress label returns to idle after cancellation."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "Soal 1 dari 3",
        )

        self.quiz_tab.cancel_quiz()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            self.quiz_tab.progress_label.text(),
            "—",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )