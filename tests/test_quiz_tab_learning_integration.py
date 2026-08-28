"""
Integration tests for QuizTab -> Learning Engine.

These tests verify the public QuizTab boundary together with the real
Learning Engine persistence stack. QuizTab's removed correct_count,
incorrect_count, session, and private question state are intentionally
not used.
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
from core.learning.repositories.learner_repository import (
    StorageLearnerRepository,
)
from core.learning.services.learning_service import LearningService
from core.learning.storage.json_adapter import JSONAdapter
from application.learning.quiz.quiz_difficulty import QuizDifficulty
from ui.tabs.quiz_tab import QuizTab


class FakeQuizGenerator:
    """Deterministic QuizGenerator test double."""

    def __init__(self):
        self.question = SimpleNamespace(
            prompt="ꦲ",
            correct_answer="ha",
            options=("ha", "na", "ca", "ra"),
        )

    def generate(self, difficulty):
        return self.question


class TestQuizTabLearningIntegration(unittest.TestCase):
    """Test QuizTab integration with the real Learning Engine."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        storage = JSONAdapter(
            self.temp_dir,
        )

        self.repository = StorageLearningRepository(
            storage,
        )

        self.learner_repository = StorageLearnerRepository(
            storage,
        )

        self.learning_service = LearningService(
            self.repository,
            self.learner_repository,
        )
        self.generator = FakeQuizGenerator()
        self.quiz_tab = QuizTab(
            generator=self.generator,
            learning_service=self.learning_service,
            learner_id="learner-001",
        )

    def tearDown(self):
        print(f"\nBEFORE CLEANUP: {self.temp_dir}")
        print(f"EXISTS: {self.temp_dir.exists()}")

        self.quiz_tab.deleteLater()
        self.app.processEvents()

        print(f"BEFORE RMTREE: {self.temp_dir}")
        print(f"EXISTS: {self.temp_dir.exists()}")

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=False,
        )

        print(f"AFTER RMTREE: {self.temp_dir}")
        print(f"EXISTS: {self.temp_dir.exists()}")

    def test_completed_quiz_is_persisted_by_learning_engine(self):
        """A completed Quiz becomes one persisted StudySession."""
        self.quiz_tab.start_quiz(
            QuizDifficulty.LEVEL_1,
            total_questions=2,
        )

        self.assertTrue(self.quiz_tab.check_answer("ha"))
        self.quiz_tab.next_question()
        self.assertFalse(self.quiz_tab.check_answer("ca"))

        sessions = self.repository.load_sessions("learner-001")

        self.assertEqual(len(sessions), 1)

        session = sessions[0]
        self.assertEqual(session.learner_id, "learner-001")
        self.assertEqual(session.activity_type, ActivityType.QUIZ)

        result = session.payload
        self.assertEqual(result.total_questions, 2)
        self.assertEqual(result.correct_answers, 1)
        self.assertEqual(result.incorrect_answers, 1)
        self.assertEqual(
            result.difficulty_level,
            QuizDifficulty.LEVEL_1.value,
        )

    def test_cancelled_quiz_is_not_persisted(self):
        """A cancelled Quiz does not create learning history."""
        self.quiz_tab.start_quiz(
            QuizDifficulty.LEVEL_1,
            total_questions=2,
        )
        self.quiz_tab.select_answer("ha")
        self.quiz_tab.cancel_quiz()

        sessions = self.repository.load_sessions("learner-001")
        self.assertEqual(sessions, [])

    def test_second_completed_quiz_creates_separate_learning_session(self):
        """Each completed Quiz creates its own StudySession."""
        self.quiz_tab.start_quiz(
            QuizDifficulty.LEVEL_1,
            total_questions=1,
        )
        self.assertTrue(self.quiz_tab.check_answer("ha"))

        self.quiz_tab.retry_quiz()
        self.assertTrue(self.quiz_tab.check_answer("ha"))

        sessions = self.repository.load_sessions("learner-001")

        self.assertEqual(len(sessions), 2)
        self.assertNotEqual(
            sessions[0].session_id,
            sessions[1].session_id,
        )
        self.assertEqual(sessions[0].activity_type, ActivityType.QUIZ)
        self.assertEqual(sessions[1].activity_type, ActivityType.QUIZ)
        self.assertEqual(sessions[0].payload.total_questions, 1)
        self.assertEqual(sessions[1].payload.total_questions, 1)

    def test_persisted_result_matches_quiz_statistics(self):
        """
        Persisted QuizResult matches the expected QuizSession statistics.

        The deterministic scenario contains one correct and one incorrect
        answer. Statistics are owned by QuizSession, not QuizTab.
        """
        expected_total = 2
        expected_correct = 1
        expected_incorrect = 1

        self.quiz_tab.start_quiz(
            QuizDifficulty.LEVEL_1,
            total_questions=expected_total,
        )

        self.assertTrue(self.quiz_tab.check_answer("ha"))
        self.quiz_tab.next_question()
        self.assertFalse(self.quiz_tab.check_answer("na"))

        sessions = self.repository.load_sessions("learner-001")

        self.assertEqual(len(sessions), 1)

        result = sessions[0].payload

        self.assertEqual(result.total_questions, expected_total)
        self.assertEqual(result.correct_answers, expected_correct)
        self.assertEqual(result.incorrect_answers, expected_incorrect)
        self.assertEqual(
            result.difficulty_level,
            QuizDifficulty.LEVEL_1.value,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
