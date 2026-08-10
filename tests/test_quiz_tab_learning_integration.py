"""
Integration tests for QuizTab -> Learning Engine.
"""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from types import SimpleNamespace


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from PySide6.QtWidgets import QApplication

from core.learning.models.activity import ActivityType
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.services.learning_service import LearningService
from core.learning.storage.json_storage import JSONStorage

from application.learning.quiz.quiz_difficulty import QuizDifficulty

from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Deterministic QuizGenerator test double."""

    def __init__(self):
        self.question = SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=(
                "ha",
                "na",
                "ca",
                "ra",
            ),
        )

    def generate(self, difficulty):
        return self.question


class TestQuizTabLearningIntegration(unittest.TestCase):
    """Test QuizTab integration with the real Learning Engine."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()

        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        self.temp_dir = Path(
            tempfile.mkdtemp()
        )

        self.storage = JSONStorage(
            self.temp_dir,
        )

        self.repository = StorageLearningRepository(
            self.storage,
        )

        self.learning_service = LearningService(
            self.repository,
        )

        self.generator = FakeQuizGenerator()

        self.quiz_tab = QuizTab(
            generator=self.generator,
            learning_service=self.learning_service,
            learner_id="learner-001",
        )

    def tearDown(self):
        self.quiz_tab.deleteLater()

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    def test_completed_quiz_is_persisted_by_learning_engine(self):
        """
        A completed QuizTab session becomes one persisted StudySession.
        """

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        # Question 1 — correct.
        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        # Question 2 — incorrect.
        self.quiz_tab.select_answer("ca")
        self.quiz_tab.submit_answer("ca")
        self.quiz_tab.next_question()

        sessions = self.repository.load_sessions()

        self.assertEqual(
            len(sessions),
            1,
        )

        session = sessions[0]

        self.assertEqual(
            session.activity_type,
            ActivityType.QUIZ,
        )

        result = session.payload

        self.assertEqual(
            result.total_questions,
            2,
        )

        self.assertEqual(
            result.correct_answers,
            1,
        )

        self.assertEqual(
            result.incorrect_answers,
            1,
        )

    def test_cancelled_quiz_is_not_persisted(self):
        """
        A cancelled QuizTab session does not create learning history.
        """

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.quiz_tab.select_answer("ha")

        self.quiz_tab.cancel_quiz()

        sessions = self.repository.load_sessions()

        self.assertEqual(
            sessions,
            [],
        )

    def test_second_completed_quiz_creates_separate_learning_session(self):
        """
        Each completed Quiz creates its own StudySession.
        """

        # -------------------------------------------------
        # Quiz 1
        # -------------------------------------------------

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        answer = self.quiz_tab._current_question.correct_answer

        self.quiz_tab.select_answer(answer)
        self.quiz_tab.submit_answer(answer)
        self.quiz_tab.next_question()

        # -------------------------------------------------
        # Quiz 2
        # -------------------------------------------------

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=1,
        )

        answer = self.quiz_tab._current_question.correct_answer

        self.quiz_tab.select_answer(answer)
        self.quiz_tab.submit_answer(answer)
        self.quiz_tab.next_question()

        sessions = self.repository.load_sessions()

        self.assertEqual(
            len(sessions),
            2,
        )

        self.assertNotEqual(
            sessions[0].session_id,
            sessions[1].session_id,
        )

        self.assertEqual(
            sessions[0].activity_type,
            ActivityType.QUIZ,
        )

        self.assertEqual(
            sessions[1].activity_type,
            ActivityType.QUIZ,
        )

    def test_persisted_result_matches_quiz_statistics(self):
        """Persisted QuizResult matches QuizTab statistics."""

        self.quiz_tab.start_quiz(
            difficulty=QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        # Question 1 — correct.
        self.quiz_tab.select_answer("ha")
        self.quiz_tab.submit_answer("ha")
        self.quiz_tab.next_question()

        # Question 2 — incorrect.
        self.quiz_tab.select_answer("na")
        self.quiz_tab.submit_answer("na")

        expected_correct = self.quiz_tab.correct_count
        expected_incorrect = self.quiz_tab.incorrect_count

        self.assertEqual(
            expected_correct,
            1,
        )

        self.assertEqual(
            expected_incorrect,
            1,
        )

        # Completing the final question persists the result
        # and resets QuizTab statistics to idle state.
        self.quiz_tab.next_question()

        sessions = self.repository.load_sessions()

        self.assertEqual(
            len(sessions),
            1,
        )

        result = sessions[0].payload

        self.assertEqual(
            result.total_questions,
            2,
        )

        self.assertEqual(
            result.correct_answers,
            expected_correct,
        )

        self.assertEqual(
            result.incorrect_answers,
            expected_incorrect,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )