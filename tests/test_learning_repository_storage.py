"""
Integration tests for LearningRepository with JSONAdapter.

Architecture references:
    AD-LE-006 — Persistence operations SHALL be performed through
                Learning Repository.
    AD-LE-009 — Learning Engine SHALL NOT depend on a specific
                storage technology.
"""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from typing import Any


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
from core.learning.models.learner_identity import LearnerIdentity
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.storage.json_adapter import JSONAdapter
from application.learning.quiz.quiz_difficulty import QuizDifficulty


class FailingStorage:
    """Storage double that fails on save()."""

    def load(self, key):
        return None

    def save(self, key, data):
        raise OSError("Simulated storage failure")

    def delete(self, key):
        pass

    def exists(self, key):
        return False


class TestStorageLearningRepository(unittest.TestCase):
    """Test LearningRepository persistence using JSONAdapter."""

    def setUp(self) -> None:
        """Create an isolated temporary repository."""

        self.temp_dir = Path(tempfile.mkdtemp())

        storage = JSONAdapter(
            self.temp_dir,
        )

        self.repository = StorageLearningRepository(
            storage,
        )

    def tearDown(self) -> None:
        """Remove temporary storage."""

        shutil.rmtree(
            self.temp_dir,
            ignore_errors=True,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_session(
        self,
        session_id: str = "session-001",
        learner_id: str = "learner-001",
    ) -> StudySession:
        """Create a valid Quiz StudySession."""

        return StudySession(
            session_id=session_id,
            learner_id=learner_id,
            timestamp=datetime(
                2026,
                8,
                9,
                10,
                30,
                tzinfo=timezone.utc,
            ),
            activity_type=ActivityType.QUIZ,
            payload=QuizResult(
                difficulty_level=1,
                total_questions=10,
                correct_answers=8,
                incorrect_answers=2,
            ),
        )

    # ------------------------------------------------------------------
    # Learner Identity
    # ------------------------------------------------------------------

    def save_learner(
        self,
        learner: LearnerIdentity,
    ) -> None:
        """
        Persist a LearnerIdentity.

        Learners are stored by learner identifier.
        """

        learners = self.storage.load(
            self.LEARNERS_KEY,
        )

        if learners is None:
            learners = {}

        learners[learner.learner_id] = self._serialize_learner(
            learner,
        )

        self.storage.save(
            self.LEARNERS_KEY,
            learners,
        )

    def load_learner(
        self,
        learner_id: str,
    ) -> LearnerIdentity | None:
        """
        Load a LearnerIdentity by learner ID.

        Returns:
            Reconstructed LearnerIdentity or None.
        """

        learners = self.storage.load(
            self.LEARNERS_KEY,
        )

        if learners is None:
            return None

        data = learners.get(learner_id)

        if data is None:
            return None

        return self._deserialize_learner(
            data,
        )

    # ------------------------------------------------------------------
    # StudySession
    # ------------------------------------------------------------------

    def test_save_and_load_session_round_trip(self):
        """A StudySession survives a complete persistence round-trip."""

        original = self._create_session()

        self.repository.save_session(
            original,
        )

        loaded_sessions = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(loaded_sessions),
            1,
        )

        loaded = loaded_sessions[0]

        self.assertEqual(
            loaded.session_id,
            original.session_id,
        )

        self.assertEqual(
            loaded.timestamp,
            original.timestamp,
        )

        self.assertIs(
            loaded.activity_type,
            ActivityType.QUIZ,
        )

        self.assertIsInstance(
            loaded.payload,
            QuizResult,
        )

        self.assertEqual(
            loaded.payload.total_questions,
            original.payload.total_questions,
        )

        self.assertEqual(
            loaded.payload.correct_answers,
            original.payload.correct_answers,
        )

        self.assertEqual(
            loaded.payload.incorrect_answers,
            original.payload.incorrect_answers,
        )

    def test_multiple_sessions_round_trip(self):
        """Multiple StudySession records survive persistence."""

        session_1 = self._create_session(
            "session-001",
        )

        session_2 = self._create_session(
            "session-002",
        )

        self.repository.save_session(
            session_1,
        )

        self.repository.save_session(
            session_2,
        )

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(loaded),
            2,
        )

        self.assertEqual(
            [session.session_id for session in loaded],
            [
                "session-001",
                "session-002",
            ],
        )

    def test_sessions_are_isolated_by_learner(self):
        """Loading sessions returns only records belonging to the learner."""

        learner_a_session_1 = self._create_session(
            session_id="session-001",
            learner_id="learner-001",
        )

        learner_b_session = self._create_session(
            session_id="session-002",
            learner_id="learner-002",
        )

        learner_a_session_2 = self._create_session(
            session_id="session-003",
            learner_id="learner-001",
        )

        self.repository.save_session(
            learner_a_session_1,
        )

        self.repository.save_session(
            learner_b_session,
        )

        self.repository.save_session(
            learner_a_session_2,
        )

        sessions = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(sessions),
            2,
        )

        self.assertEqual(
            {session.session_id for session in sessions},
            {
                "session-001",
                "session-003",
            },
        )

        self.assertTrue(
            all(
                session.learner_id == "learner-001"
                for session in sessions
            )
        )

    def test_session_update_replaces_same_session(self):
        """Saving the same session ID replaces the previous record."""

        original = self._create_session(
            "session-001",
        )

        updated = StudySession(
            session_id="session-001",
            learner_id="learner-001",
            timestamp=datetime(
                2026,
                8,
                9,
                11,
                30,
                tzinfo=timezone.utc,
            ),
            activity_type=ActivityType.QUIZ,
            payload=QuizResult(
                difficulty_level=2,
                total_questions=20,
                correct_answers=18,
                incorrect_answers=2,
            ),
        )

        self.repository.save_session(
            original,
        )

        self.repository.save_session(
            updated,
        )

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            len(loaded),
            1,
        )

        self.assertEqual(
            loaded[0].session_id,
            "session-001",
        )

        self.assertEqual(
            loaded[0].payload.total_questions,
            20,
        )

    # ------------------------------------------------------------------
    # LearningProfile
    # ------------------------------------------------------------------

    def test_save_and_load_profile_round_trip(self):
        """A LearningProfile survives a complete persistence round-trip."""

        timestamp = datetime(
            2026,
            8,
            9,
            12,
            0,
            tzinfo=timezone.utc,
        )

        original = LearningProfile(
            learner_id="learner-001",
            total_sessions=5,
            total_questions=50,
            correct_answers=42,
            incorrect_answers=8,
            last_activity=timestamp,
        )

        self.repository.save_profile(
            original,
        )

        loaded = self.repository.load_profile(
            "learner-001",
        )

        self.assertIsNotNone(
            loaded,
        )

        self.assertEqual(
            loaded.learner_id,
            original.learner_id,
        )

        self.assertEqual(
            loaded.total_sessions,
            original.total_sessions,
        )

        self.assertEqual(
            loaded.total_questions,
            original.total_questions,
        )

        self.assertEqual(
            loaded.correct_answers,
            original.correct_answers,
        )

        self.assertEqual(
            loaded.incorrect_answers,
            original.incorrect_answers,
        )

        self.assertEqual(
            loaded.last_activity,
            original.last_activity,
        )

    def test_multiple_profiles_round_trip(self):
        """Multiple learner profiles survive persistence."""

        profile_1 = LearningProfile(
            learner_id="learner-001",
            total_sessions=2,
            total_questions=20,
            correct_answers=16,
            incorrect_answers=4,
        )

        profile_2 = LearningProfile(
            learner_id="learner-002",
            total_sessions=3,
            total_questions=30,
            correct_answers=27,
            incorrect_answers=3,
        )

        self.repository.save_profile(
            profile_1,
        )

        self.repository.save_profile(
            profile_2,
        )

        loaded_1 = self.repository.load_profile(
            "learner-001",
        )

        loaded_2 = self.repository.load_profile(
            "learner-002",
        )

        self.assertIsNotNone(loaded_1)
        self.assertIsNotNone(loaded_2)

        self.assertEqual(
            loaded_1.total_sessions,
            2,
        )

        self.assertEqual(
            loaded_2.total_sessions,
            3,
        )

    def test_missing_profile_returns_none(self):
        """A missing learner profile returns None."""

        loaded = self.repository.load_profile(
            "unknown-learner",
        )

        self.assertIsNone(
            loaded,
        )

    # ------------------------------------------------------------------
    # Unicode
    # ------------------------------------------------------------------

    def test_session_persistence_preserves_unicode_payload(self):
        """
        Repository persistence must preserve Unicode data.

        This test uses a Unicode learner identifier to verify that
        JSON persistence does not corrupt non-ASCII text.
        """

        session = self._create_session(
            "ꦲꦤꦕꦫꦏ",
        )

        self.repository.save_session(
            session,
        )

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            loaded[0].session_id,
            "ꦲꦤꦕꦫꦏ",
        )

    def test_save_session_propagates_storage_failure(self):
        """Storage failures are propagated to the caller."""

        repository = StorageLearningRepository(
            FailingStorage(),
        )

        session = self._create_session()

        with self.assertRaises(OSError):
            repository.save_session(
                session,
            )

    @staticmethod
    def _serialize_learner(
        learner: LearnerIdentity,
    ) -> dict[str, Any]:
        """
        Convert a LearnerIdentity into storage-neutral data.
        """

        return {
            "learner_id": learner.learner_id,
            "display_name": learner.display_name,
            "is_guest": learner.is_guest,
        }

    @staticmethod
    def _deserialize_learner(
        data: dict[str, Any],
    ) -> LearnerIdentity:
        """
        Reconstruct a LearnerIdentity from stored data.
        """

        return LearnerIdentity(
            learner_id=data["learner_id"],
            display_name=data["display_name"],
            is_guest=data["is_guest"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)