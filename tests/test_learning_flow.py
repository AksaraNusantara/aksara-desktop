"""
End-to-end integration tests for the AD-7 Learning Engine flow.

Architecture references:
    AD-LE-001 — LearningProfile is a derived aggregate.
    AD-LE-002 — StudySession is primary learning activity data.
    AD-LE-006 — Persistence uses LearningRepository.
    AD-LE-007 — LearningService coordinates learning logic.
    AD-LE-008 — Statistics are derived data.
    AD-LE-009 — Storage technology is isolated behind StorageAdapter.
"""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from core.learning.models.activity import ActivityType
from core.learning.models.payload import QuizResult
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.services.learning_service import LearningService
from core.learning.services.statistics_service import (
    StatisticsService,
)
from core.learning.storage.json_storage import JSONStorage


class TestLearningFlow(unittest.TestCase):
    """
    Validate the complete AD-7 learning flow.

    The test intentionally uses the real JSONStorage and
    StorageLearningRepository implementations.
    """

    def setUp(self) -> None:
        """Create an isolated Learning Engine environment."""

        self.temp_dir = Path(tempfile.mkdtemp())

        storage = JSONStorage(
            self.temp_dir,
        )

        repository = StorageLearningRepository(
            storage,
        )

        self.learning_service = LearningService(
            repository,
        )

        self.statistics_service = StatisticsService()

        self.repository = repository

    def tearDown(self) -> None:
        """Remove temporary persistent data."""

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    def test_complete_quiz_learning_flow(self):
        """
        A completed Quiz flows through the entire Learning Engine.

        Expected flow:

            QuizResult
                ↓
            LearningService
                ↓
            StudySession
                ↓
            LearningProfile
                ↓
            JSONStorage
                ↓
            reload
                ↓
            StatisticsService
        """

        learner_id = "learner-001"

        timestamp = datetime(
            2026,
            8,
            9,
            10,
            30,
            tzinfo=timezone.utc,
        )

        result = QuizResult(
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        # --------------------------------------------------------------
        # 1. Record completed Quiz
        # --------------------------------------------------------------

        session = self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=result,
            timestamp=timestamp,
        )

        # --------------------------------------------------------------
        # 2. Verify StudySession
        # --------------------------------------------------------------

        self.assertEqual(
            session.activity_type,
            ActivityType.QUIZ,
        )

        self.assertEqual(
            session.payload,
            result,
        )

        # --------------------------------------------------------------
        # 3. Verify persisted StudySession
        # --------------------------------------------------------------

        sessions = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(sessions),
            1,
        )

        self.assertEqual(
            sessions[0].session_id,
            session.session_id,
        )

        # --------------------------------------------------------------
        # 4. Verify LearningProfile
        # --------------------------------------------------------------

        profile = self.repository.load_profile(
            learner_id,
        )

        self.assertIsNotNone(
            profile,
        )

        self.assertEqual(
            profile.total_sessions,
            1,
        )

        self.assertEqual(
            profile.total_questions,
            10,
        )

        self.assertEqual(
            profile.correct_answers,
            8,
        )

        self.assertEqual(
            profile.incorrect_answers,
            2,
        )

        # --------------------------------------------------------------
        # 5. Calculate derived Statistics
        # --------------------------------------------------------------

        statistics = self.statistics_service.calculate(
            profile,
        )

        self.assertEqual(
            statistics.total_sessions,
            1,
        )

        self.assertEqual(
            statistics.total_questions,
            10,
        )

        self.assertEqual(
            statistics.correct_answers,
            8,
        )

        self.assertEqual(
            statistics.incorrect_answers,
            2,
        )

        self.assertEqual(
            statistics.accuracy,
            80.0,
        )

    def test_multiple_quizzes_produce_correct_aggregate(self):
        """
        Multiple Quiz activities accumulate correctly across the
        complete Learning Engine flow.
        """

        learner_id = "learner-001"

        self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=QuizResult(
                total_questions=10,
                correct_answers=8,
                incorrect_answers=2,
            ),
            timestamp=datetime(
                2026,
                8,
                9,
                10,
                0,
                tzinfo=timezone.utc,
            ),
        )

        self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=QuizResult(
                total_questions=20,
                correct_answers=15,
                incorrect_answers=5,
            ),
            timestamp=datetime(
                2026,
                8,
                9,
                11,
                0,
                tzinfo=timezone.utc,
            ),
        )

        self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=QuizResult(
                total_questions=5,
                correct_answers=4,
                incorrect_answers=1,
            ),
            timestamp=datetime(
                2026,
                8,
                9,
                12,
                0,
                tzinfo=timezone.utc,
            ),
        )

        # --------------------------------------------------------------
        # Verify Primary Data
        # --------------------------------------------------------------

        sessions = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(sessions),
            3,
        )

        # --------------------------------------------------------------
        # Verify derived aggregate
        # --------------------------------------------------------------

        profile = self.repository.load_profile(
            learner_id,
        )

        self.assertIsNotNone(
            profile,
        )

        self.assertEqual(
            profile.total_sessions,
            3,
        )

        self.assertEqual(
            profile.total_questions,
            35,
        )

        self.assertEqual(
            profile.correct_answers,
            27,
        )

        self.assertEqual(
            profile.incorrect_answers,
            8,
        )

        # --------------------------------------------------------------
        # Verify derived statistics
        # --------------------------------------------------------------

        statistics = self.statistics_service.calculate(
            profile,
        )

        self.assertEqual(
            statistics.accuracy,
            27 / 35 * 100,
        )

    def test_profile_can_be_reconstructed_from_sessions(self):
        """
        LearningProfile can be reconstructed from StudySession data.

        This validates the Source of Truth principle:

            StudySession = authoritative history
            LearningProfile = derived aggregate
        """

        learner_id = "learner-001"

        self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=QuizResult(
                total_questions=10,
                correct_answers=7,
                incorrect_answers=3,
            ),
            timestamp=datetime(
                2026,
                8,
                9,
                10,
                0,
                tzinfo=timezone.utc,
            ),
        )

        self.learning_service.record_quiz_result(
            learner_id=learner_id,
            result=QuizResult(
                total_questions=20,
                correct_answers=18,
                incorrect_answers=2,
            ),
            timestamp=datetime(
                2026,
                8,
                9,
                11,
                0,
                tzinfo=timezone.utc,
            ),
        )

        sessions = self.repository.load_sessions(
            "learner-001",
        )

        reconstructed_total_sessions = len(sessions)

        reconstructed_total_questions = sum(
            session.payload.total_questions
            for session in sessions
            if session.activity_type is ActivityType.QUIZ
        )

        reconstructed_correct_answers = sum(
            session.payload.correct_answers
            for session in sessions
            if session.activity_type is ActivityType.QUIZ
        )

        reconstructed_incorrect_answers = sum(
            session.payload.incorrect_answers
            for session in sessions
            if session.activity_type is ActivityType.QUIZ
        )

        self.assertEqual(
            reconstructed_total_sessions,
            2,
        )

        self.assertEqual(
            reconstructed_total_questions,
            30,
        )

        self.assertEqual(
            reconstructed_correct_answers,
            25,
        )

        self.assertEqual(
            reconstructed_incorrect_answers,
            5,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)