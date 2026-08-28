"""Contract tests for LearningRepository.

This file is the full candidate replacement for
tests/test_learning_repository.py.

The test fixture follows the current QuizResult contract and uses
JSONAdapter, not the retired JSONAdapter name.
"""

from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

#from application.learning.quiz.quiz_difficulty import QuizDifficulty
from core.learning.models.activity import ActivityType
from core.learning.models.learning_profile import LearningProfile
from core.learning.models.payload import QuizResult
from core.learning.models.study_session import StudySession
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.storage.json_adapter import JSONAdapter


class TestLearningRepositoryContract(unittest.TestCase):
    """Validate StudySession and LearningProfile persistence."""

    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()

        self.storage_path = (
            Path(self._temp_dir.name) / "learning.json"
        )

        self.storage = JSONAdapter(self.storage_path)

        self.repository = StorageLearningRepository(
            self.storage,
        )

    def tearDown(self):
        self._temp_dir.cleanup()

    def _create_session(
        self,
        session_id: str = "session-001",
        learner_id: str = "learner-001",
        difficulty_level: int = 1,
    ) -> StudySession:
        """Create a valid Quiz StudySession for repository tests."""

        return StudySession(
            session_id=session_id,
            learner_id=learner_id,
            timestamp=datetime.now(timezone.utc),
            activity_type=ActivityType.QUIZ,
            payload=QuizResult(
                difficulty_level=difficulty_level,
                total_questions=10,
                correct_answers=8,
                incorrect_answers=2,
            ),
        )

    def _create_profile(
        self,
        learner_id: str = "learner-001",
    ) -> LearningProfile:
        """Create a valid LearningProfile for repository tests."""

        return LearningProfile(
            learner_id=learner_id,
            total_sessions=3,
            total_questions=30,
            correct_answers=24,
            incorrect_answers=6,
            last_activity=datetime.now(timezone.utc),
        )

    def test_save_and_load_session(self):
        """A saved StudySession can be loaded."""

        session = self._create_session()

        self.repository.save_session(session)

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            [session],
        )

    def test_multiple_sessions_are_preserved(self):
        """Multiple StudySession records are preserved."""

        session_1 = self._create_session(
            session_id="session-001",
            learner_id="learner-001",
        )

        session_2 = self._create_session(
            session_id="session-002",
            learner_id="learner-001",
            difficulty_level=2,
        )

        self.repository.save_session(session_1)
        self.repository.save_session(session_2)

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            [session_1, session_2],
        )

    def test_sessions_are_isolated_by_learner(self):
        """Loading sessions returns only records for that learner."""

        learner_a_session_1 = self._create_session(
            session_id="session-001",
            learner_id="learner-001",
        )

        learner_a_session_2 = self._create_session(
            session_id="session-002",
            learner_id="learner-001",
            difficulty_level=2,
        )

        learner_b_session = self._create_session(
            session_id="session-003",
            learner_id="learner-002",
        )

        self.repository.save_session(
            learner_a_session_1,
        )
        self.repository.save_session(
            learner_a_session_2,
        )
        self.repository.save_session(
            learner_b_session,
        )

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            [
                learner_a_session_1,
                learner_a_session_2,
            ],
        )

    def test_replacing_session_with_same_id(self):
        """Saving the same session ID replaces the previous session."""

        original = self._create_session(
            session_id="session-001",
            learner_id="learner-001",
            difficulty_level=1,
        )

        replacement = self._create_session(
            session_id="session-001",
            learner_id="learner-001",
            difficulty_level=3,
        )

        self.repository.save_session(original)
        self.repository.save_session(replacement)

        loaded = self.repository.load_sessions(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            [replacement],
        )

    def test_missing_sessions_returns_empty_list(self):
        """A learner without sessions receives an empty list."""

        self.assertEqual(
            self.repository.load_sessions(
                "missing-learner",
            ),
            [],
        )

    def test_save_and_load_profile(self):
        """A saved LearningProfile can be loaded."""

        profile = self._create_profile()

        self.repository.save_profile(profile)

        loaded = self.repository.load_profile(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            profile,
        )

    def test_missing_profile_returns_none(self):
        """A missing LearningProfile returns None."""

        self.assertIsNone(
            self.repository.load_profile(
                "missing-learner",
            ),
        )

    def test_profile_is_replaced_by_learner_id(self):
        """Saving a profile with the same learner ID replaces it."""

        original = self._create_profile(
            "learner-001",
        )

        replacement = LearningProfile(
            learner_id="learner-001",
            total_sessions=7,
            total_questions=70,
            correct_answers=63,
            incorrect_answers=7,
            last_activity=datetime.now(timezone.utc),
        )

        self.repository.save_profile(original)
        self.repository.save_profile(replacement)

        loaded = self.repository.load_profile(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            replacement,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
