"""
Tests for QuizTab progress state.
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
                options=("ha", "na", "ca", "ra"),
            ),
            SimpleNamespace(
                prompt="ꦤ",
                correct_answer="na",
                options=("na", "ca", "ra", "ka"),
            ),
            SimpleNamespace(
                prompt="ꦕ",
                correct_answer="ca",
                options=("ca", "ra", "ka", "da"),
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


class TestQuizTabProgress(unittest.TestCase):
    """Test QuizTab progress state."""

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

    def test_progress_is_idle_before_quiz(self):
        """Progress is empty before a Quiz starts."""

        self.assertEqual(
            self.quiz_tab.progress_text,
            "—",
        )

    def test_progress_starts_at_first_question(self):
        """Quiz starts at question one."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 3",
        )

    def test_progress_remains_on_current_question_during_feedback(self):
        """Feedback does not advance Quiz progress."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 3",
        )

    def test_progress_advances_after_next_question(self):
        """Next question advances Quiz progress."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 2 dari 3",
        )

    def test_progress_reaches_final_question(self):
        """Progress reaches the final question correctly."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=3,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()
        self.quiz_tab.next_question()

        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer()
        self.quiz_tab.next_question()

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 3 dari 3",
        )

    def test_progress_resets_after_quiz_completion(self):
        """Progress returns to idle after Quiz completion."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer()

        self.assertEqual(
            self.quiz_tab.progress_text,
            "—",
        )

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )
        self.assertEqual(
            self.quiz_tab.progress_text,
            "—",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )