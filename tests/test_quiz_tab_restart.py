"""
Tests for QuizTab new Quiz / restart flow.
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


class TestQuizTabRestart(unittest.TestCase):
    """Test starting a new Quiz after completion."""

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

    def _complete_quiz(self):
        """Complete the current one-question Quiz."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")
        self.quiz_tab.next_question()

    def test_new_quiz_can_start_after_completion(self):
        """A new Quiz can start after the previous Quiz completes."""

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.assertTrue(
            self.quiz_tab.is_quiz_active,
        )

    def test_new_quiz_starts_at_first_question(self):
        """A new Quiz starts from question one."""

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 2",
        )

    def test_new_quiz_resets_statistics(self):
        """A new Quiz starts with fresh statistics."""

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.assertEqual(self.quiz_tab.accuracy_text, "0%")

        self.assertEqual(self.quiz_tab.accuracy_text, "0%")

        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )

    def test_new_quiz_resets_feedback(self):
        """A new Quiz does not inherit previous feedback."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")

        self.assertTrue(
            self.quiz_tab.feedback_visible,
        )

        self.quiz_tab.next_question()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

    def test_new_quiz_uses_new_difficulty(self):
        """A new Quiz uses the newly selected difficulty."""

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_3,
            total_questions=2,
        )

        self.assertEqual(
            self.generator.calls[-1],
            QuizDifficulty.LEVEL_3,
        )

    def test_new_quiz_generates_new_question(self):
        """Starting a new Quiz generates a new question."""

        initial_calls = len(
            self.generator.calls,
        )

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_2,
            total_questions=2,
        )

        self.assertEqual(
            len(self.generator.calls),
            initial_calls + 2,
        )

    def test_new_quiz_can_complete_normally(self):
        """A new Quiz can complete and persist its own result."""

        self._complete_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer("na")
        self.quiz_tab.next_question()

        self.assertFalse(
            self.quiz_tab.is_quiz_active,
        )

        self.assertEqual(
            len(self.learning_service.calls),
            2,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )