"""
Tests for the Learning Engine repository contract.

Architecture references:
    AD-LE-006 — All persistence operations SHALL be performed
                through Learning Repository.
    AD-LE-009 — Learning Engine SHALL NOT depend on a specific
                storage technology.
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
# Learning Engine imports
# ---------------------------------------------------------------------------

from core.learning.models.activity import ActivityType
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.repositories.learning_repository import LearningRepository


class InMemoryLearningRepository(LearningRepository):
    """
    In-memory implementation used to validate the repository contract.

    This implementation deliberately contains no storage technology
    concerns. It exists only for contract testing.
    """

    def __init__(self) -> None:
        """Initialize the in-memory repository."""

        self._sessions: list[StudySession] = []
        self._profiles: dict[str, LearningProfile] = {}

    def save_session(self, session: StudySession) -> None:
        """Persist a StudySession in memory."""

        self._sessions.append(session)

    def load_sessions(self) -> list[StudySession]:
        """Return all persisted StudySession records."""

        return list(self._sessions)

    def save_profile(self, profile: LearningProfile) -> None:
        """Persist a LearningProfile in memory."""

        self._profiles[profile.learner_id] = profile

    def load_profile(
        self,
        learner_id: str,
    ) -> LearningProfile | None:
        """Return a persisted LearningProfile for a learner."""

        return self._profiles.get(learner_id)


class TestLearningRepositoryContract(unittest.TestCase):
    """Validate the LearningRepository contract."""

    def setUp(self) -> None:
        """Create a fresh repository for each test."""

        self.repository = InMemoryLearningRepository()

    def _create_session(
        self,
        session_id: str = "session-001",
    ) -> StudySession:
        """Create a valid Quiz StudySession."""

        return StudySession(
            session_id=session_id,
            timestamp=datetime.now(timezone.utc),
            activity_type=ActivityType.QUIZ,
            payload=QuizResult(
                total_questions=10,
                correct_answers=8,
                incorrect_answers=2,
            ),
        )

    def test_repository_is_a_learning_repository(self):
        """The implementation must satisfy the repository contract."""

        self.assertIsInstance(
            self.repository,
            LearningRepository,
        )

    def test_save_and_load_session(self):
        """A saved StudySession can be loaded."""

        session = self._create_session()

        self.repository.save_session(session)

        sessions = self.repository.load_sessions()

        self.assertEqual(len(sessions), 1)
        self.assertIs(sessions[0], session)

    def test_multiple_sessions_are_preserved(self):
        """Multiple StudySession records are preserved."""

        session_1 = self._create_session("session-001")
        session_2 = self._create_session("session-002")

        self.repository.save_session(session_1)
        self.repository.save_session(session_2)

        sessions = self.repository.load_sessions()

        self.assertEqual(len(sessions), 2)
        self.assertEqual(
            [session.session_id for session in sessions],
            ["session-001", "session-002"],
        )

    def test_load_sessions_returns_empty_list_initially(self):
        """A new repository has no StudySession records."""

        sessions = self.repository.load_sessions()

        self.assertEqual(sessions, [])

    def test_save_and_load_profile(self):
        """A saved LearningProfile can be loaded."""

        profile = LearningProfile(
            learner_id="learner-001",
            total_sessions=2,
            total_questions=20,
            correct_answers=16,
            incorrect_answers=4,
        )

        self.repository.save_profile(profile)

        loaded = self.repository.load_profile("learner-001")

        self.assertIs(loaded, profile)

    def test_load_missing_profile_returns_none(self):
        """Loading a non-existent profile returns None."""

        loaded = self.repository.load_profile("unknown-learner")

        self.assertIsNone(loaded)

    def test_profile_is_replaced_for_same_learner(self):
        """Saving a profile replaces the previous aggregate."""

        profile_1 = LearningProfile(
            learner_id="learner-001",
            total_sessions=1,
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        profile_2 = LearningProfile(
            learner_id="learner-001",
            total_sessions=2,
            total_questions=20,
            correct_answers=17,
            incorrect_answers=3,
        )

        self.repository.save_profile(profile_1)
        self.repository.save_profile(profile_2)

        loaded = self.repository.load_profile("learner-001")

        self.assertIs(loaded, profile_2)
        self.assertEqual(loaded.total_sessions, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)