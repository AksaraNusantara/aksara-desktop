"""
Learning Service learner identity integration tests.
"""

import sys
import tempfile
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.learning.models.learner_identity import LearnerIdentity
from core.learning.repositories.learning_repository import (
    StorageLearningRepository,
)
from core.learning.repositories.learner_repository import (
    StorageLearnerRepository,
)
from core.learning.services.learning_service import LearningService
from core.learning.storage.json_adapter import JSONAdapter
from core.learning.models.payload import QuizResult

from application.learning.quiz.quiz_difficulty import QuizDifficulty


class TestLearningServiceIdentity(unittest.TestCase):
    """Test learner identity integration in LearningService."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

        storage = JSONAdapter(
            self.temp_dir.name,
        )

        self.repository = StorageLearningRepository(
            storage,
        )

        self.learner_repository = StorageLearnerRepository(
            storage,
        )

        self.service = LearningService(
            self.repository,
            self.learner_repository,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_named_learner_can_be_registered(self):
        """A named learner can be registered through the service."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        self.service.register_learner(
            learner,
        )

        loaded = self.service.get_learner(
            learner.learner_id,
        )

        self.assertEqual(
            loaded,
            learner,
        )

    def test_guest_learner_can_be_registered(self):
        """A Guest learner can be registered through the service."""

        learner = LearnerIdentity(
            learner_id="guest-001",
            display_name="Guest",
            is_guest=True,
        )

        self.service.register_learner(
            learner,
        )

        loaded = self.service.get_learner(
            learner.learner_id,
        )

        self.assertEqual(
            loaded,
            learner,
        )

    def test_missing_learner_returns_none(self):
        """A missing learner returns None."""

        loaded = self.service.get_learner(
            "missing-learner",
        )

        self.assertIsNone(
            loaded,
        )

    def test_same_learner_id_replaces_previous_identity(self):
        """Registering the same ID replaces the previous identity."""

        first = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        second = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi Santoso",
            is_guest=False,
        )

        self.service.register_learner(
            first,
        )

        self.service.register_learner(
            second,
        )

        loaded = self.service.get_learner(
            "learner-001",
        )

        self.assertEqual(
            loaded,
            second,
        )

    def test_registered_learner_can_record_quiz_result(self):
        """A registered learner can record a Quiz result."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        self.service.register_learner(
            learner,
        )

        result = QuizResult(
            difficulty_level=QuizDifficulty.LEVEL_1.value,
            total_questions=10,
            correct_answers=8,
            incorrect_answers=2,
        )

        session = self.service.record_quiz_result(
            learner_id=learner.learner_id,
            result=result,
        )

        self.assertEqual(
            session.learner_id,
            learner.learner_id,
        )

        profile = self.repository.load_profile(
            learner.learner_id,
        )

        self.assertIsNotNone(profile)

        self.assertEqual(
            profile.learner_id,
            learner.learner_id,
        )

        self.assertEqual(
            profile.total_sessions,
            1,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
    )
