"""
Tests for QuizTab session isolation.
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


class TestQuizTabSessionIsolation(unittest.TestCase):
    """Test isolation between separate Quiz sessions."""

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

    def _complete_first_quiz(self):
        """Complete the first Quiz with a correct answer."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("ha")
        self.quiz_tab.check_answer("ha")
        self.quiz_tab.next_question()

    def test_second_quiz_starts_with_fresh_statistics(self):
        """Second Quiz does not inherit first Quiz statistics."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )



        self.assertEqual(
            self.quiz_tab.accuracy_text,
            "0%",
        )

    def test_second_quiz_starts_without_selected_answer(self):
        """Second Quiz has no selected answer from the first Quiz."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertIsNone(
            self.quiz_tab.selected_answer,
        )

    def test_second_quiz_starts_without_feedback(self):
        """Second Quiz does not inherit feedback."""

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
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertFalse(
            self.quiz_tab.feedback_visible,
        )

    def test_second_quiz_starts_from_first_question(self):
        """Second Quiz starts from question one."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertEqual(
            self.quiz_tab.progress_text,
            "Soal 1 dari 1",
        )

    def test_second_quiz_has_independent_session(self):
        """Second Quiz creates an independent public Quiz state."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.assertTrue(self.quiz_tab.is_quiz_active)
        self.assertFalse(self.quiz_tab.is_result_visible)
        self.assertEqual(self.quiz_tab.progress_text, "Soal 1 dari 1")
        self.assertIsNone(self.quiz_tab.selected_answer)
        self.assertFalse(self.quiz_tab.feedback_visible)

    def test_second_quiz_result_is_persisted_separately(self):
        """Each completed Quiz produces its own persisted result."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer("na")
        self.quiz_tab.next_question()

        self.assertEqual(
            len(self.learning_service.calls),
            2,
        )

    def test_second_quiz_does_not_accumulate_first_quiz_score(self):
        """Second Quiz score starts independently from zero."""

        self._complete_first_quiz()

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        self.quiz_tab.select_answer("na")
        self.quiz_tab.check_answer("na")

        self.assertEqual(self.quiz_tab.accuracy_text, "100%")



if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )