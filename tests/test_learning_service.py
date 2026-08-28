"""
Tests for Learning Engine LearningService.

Architecture references:
    AD-LE-001 — LearningProfile is a derived aggregate.
    AD-LE-002 — StudySession records completed activities.
    AD-LE-006 — Persistence goes through LearningRepository.
    AD-LE-007 — LearningService coordinates learning business logic.
"""

from datetime import datetime, timezone
from pathlib import Path
import sys
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
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.learner_identity import LearnerIdentity
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.repositories.learning_repository import (
    LearningRepository,
)
from core.learning.services.learning_service import LearningService


class InMemoryLearningRepository(LearningRepository):
    """In-memory repository used for LearningService tests."""

    def __init__(self) -> None:
        """Initialize repository storage."""

        self.sessions: list[StudySession] = []
        self.profiles: dict[str, LearningProfile] = {}
        self.learners: dict[str, LearnerIdentity] = {}

    def save_learner(
        self,
        learner: LearnerIdentity,
    ) -> None:
        """Save or replace a LearnerIdentity."""

        self.learners[learner.learner_id] = learner

    def load_learner(
        self,
        learner_id: str,
    ) -> LearnerIdentity | None:
        """Load a LearnerIdentity."""

        return self.learners.get(learner_id)

    def save_session(
        self,
        session: StudySession,
    ) -> None:
        """Save or replace a StudySession."""

        self.sessions = [
            existing
            for existing in self.sessions
            if existing.session_id != session.session_id
        ]

        self.sessions.append(session)

    def load_sessions(
        self,
        learner_id: str,
    ) -> list[StudySession]:
        """Return StudySession records belonging to a learner."""

        return [
            session
            for session in self.sessions
            if session.learner_id == learner_id
        ]

    def save_profile(
        self,
        profile: LearningProfile,
    ) -> None:
        """Save a LearningProfile."""

        self.profiles[profile.learner_id] = profile

    def load_profile(
        self,
        learner_id: str,
    ) -> LearningProfile | None:
        """Load a LearningProfile."""

        return self.profiles.get(learner_id)


class FailingSessionRepository(InMemoryLearningRepository):
    """Repository that fails when saving a StudySession."""

    def save_session(
        self,
        session: StudySession,
    ) -> None:
        """Simulate a persistence failure."""

        raise OSError("Simulated session persistence failure")


class FailingProfileRepository(InMemoryLearningRepository):
    """Repository that fails when saving a learner profile."""

    def save_profile(
        self,
        profile: LearningProfile,
    ) -> None:
        """Simulate a profile persistence failure."""

        raise OSError("Simulated profile persistence failure")


class TestLearningService(unittest.TestCase):
    """Test LearningService orchestration."""

    def setUp(self) -> None:
        """Create a fresh service for each test."""

        self.repository = InMemoryLearningRepository()

        self.service = LearningService(
            self.repository,
            self.repository,
        )

        self.timestamp = datetime(
            2026,
            8,
            9,
            10,
            30,
            tzinfo=timezone.utc,
        )

    def _create_result(
        self,
        total: int = 10,
        correct: int = 8,
        incorrect: int = 2,
        difficulty_level: int = 1,
    ) -> QuizResult:
        """Create a valid QuizResult."""

        return QuizResult(
            total_questions=total,
            correct_answers=correct,
            incorrect_answers=incorrect,
            difficulty_level=difficulty_level,
        )

    def test_record_quiz_creates_study_session(self):
        """Recording a Quiz creates one StudySession."""

        result = self._create_result()

        session = self.service.record_quiz_result(
            learner_id="learner-001",
            result=result,
            timestamp=self.timestamp,
        )

        self.assertIsInstance(
            session,
            StudySession,
        )

        self.assertEqual(
            session.activity_type,
            ActivityType.QUIZ,
        )

        self.assertIs(
            session.payload,
            result,
        )

        self.assertEqual(
            session.timestamp,
            self.timestamp,
        )

    def test_record_quiz_persists_session(self):
        """The created StudySession is persisted."""

        self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(),
            timestamp=self.timestamp,
        )

        sessions = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(sessions),
            1,
        )

    def test_first_quiz_creates_profile(self):
        """The first Quiz creates a LearningProfile."""

        self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(),
            timestamp=self.timestamp,
        )

        profile = self.repository.load_profile(
            "learner-001",
        )

        self.assertIsNotNone(profile)

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

        self.assertEqual(
            profile.last_activity,
            self.timestamp,
        )

    def test_second_quiz_updates_profile(self):
        """A second Quiz accumulates into the existing profile."""

        self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(
                total=10,
                correct=8,
                incorrect=2,
            ),
            timestamp=self.timestamp,
        )

        second_timestamp = datetime(
            2026,
            8,
            9,
            11,
            30,
            tzinfo=timezone.utc,
        )

        self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(
                total=5,
                correct=4,
                incorrect=1,
            ),
            timestamp=second_timestamp,
        )

        profile = self.repository.load_profile(
            "learner-001",
        )

        self.assertEqual(
            profile.total_sessions,
            2,
        )

        self.assertEqual(
            profile.total_questions,
            15,
        )

        self.assertEqual(
            profile.correct_answers,
            12,
        )

        self.assertEqual(
            profile.incorrect_answers,
            3,
        )

        self.assertEqual(
            profile.last_activity,
            second_timestamp,
        )

    def test_empty_learner_id_is_rejected(self):
        """Learner ID must not be empty."""

        with self.assertRaises(ValueError):
            self.service.record_quiz_result(
                learner_id="",
                result=self._create_result(),
                timestamp=self.timestamp,
            )

    def test_invalid_result_type_is_rejected(self):
        """The service accepts only QuizResult for Quiz activities."""

        with self.assertRaises(TypeError):
            self.service.record_quiz_result(
                learner_id="learner-001",
                result="invalid",
                timestamp=self.timestamp,
            )

    def test_naive_timestamp_is_rejected(self):
        """Timestamps must be timezone-aware."""

        naive_timestamp = datetime(
            2026,
            8,
            9,
            10,
            30,
        )

        with self.assertRaises(ValueError):
            self.service.record_quiz_result(
                learner_id="learner-001",
                result=self._create_result(),
                timestamp=naive_timestamp,
            )

    def test_quiz_generates_unique_session_ids(self):
        """Each completed Quiz receives a unique session ID."""

        session_1 = self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(),
            timestamp=self.timestamp,
        )

        session_2 = self.service.record_quiz_result(
            learner_id="learner-001",
            result=self._create_result(),
            timestamp=self.timestamp,
        )

        self.assertNotEqual(
            session_1.session_id,
            session_2.session_id,
        )

    def test_record_quiz_propagates_session_persistence_failure(self):
        """Session persistence failures are propagated to the caller."""

        repository = FailingSessionRepository()

        service = LearningService(
            repository,
            repository,
        )

        with self.assertRaises(OSError):
            service.record_quiz_result(
                learner_id="learner-001",
                result=self._create_result(),
                timestamp=self.timestamp,
            )

    def test_record_quiz_propagates_profile_persistence_failure(self):
        """Profile persistence failures are propagated to the caller."""

        repository = FailingProfileRepository()

        service = LearningService(
            repository,
            repository,
        )

        with self.assertRaises(OSError):
            service.record_quiz_result(
                learner_id="learner-001",
                result=self._create_result(),
                timestamp=self.timestamp,
            )

    def test_record_quiz_partial_persistence_on_profile_failure(self):
        """A session may remain persisted when profile persistence fails."""

        repository = FailingProfileRepository()

        service = LearningService(
            repository,
            repository,
        )

        with self.assertRaises(OSError):
            service.record_quiz_result(
                learner_id="learner-001",
                result=self._create_result(),
                timestamp=self.timestamp,
            )

        self.assertEqual(
            len(repository.sessions),
            1,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
