"""Integration tests for persistent Application Learner ownership."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from application.application import Application
from application.application_state import ApplicationStateStorage
from core.learning.models.learner_identity import LearnerIdentity
from core.learning.repositories.learner_repository import (
    StorageLearnerRepository,
)
from core.learning.storage.json_adapter import JSONAdapter


class TestApplicationLearningPersistence(unittest.TestCase):
    """Test Active Learner persistence across Application instances."""

    def setUp(self) -> None:
        """Create isolated real storage."""

        self.temp_dir = tempfile.TemporaryDirectory()

        storage = JSONAdapter(
            self.temp_dir.name,
        )

        self.repository = StorageLearnerRepository(
            storage,
        )

        self.application_state = ApplicationStateStorage(
            storage,
        )

    def tearDown(self) -> None:
        """Remove isolated storage."""

        self.temp_dir.cleanup()

    def test_named_learner_survives_application_restart(self):
        """Named Learner can be restored by a new Application instance."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Supriyanto",
            is_guest=False,
        )

        application1 = Application(
            learner_repository=self.repository,
            application_state=self.application_state,
        )

        application1.set_active_learner(
            learner,
        )

        application2 = Application(
            learner_repository=self.repository,
            application_state=self.application_state,
        )

        application2.restore_active_learner()

        restored = application2.active_learner

        self.assertIsNotNone(
            restored,
        )

        self.assertEqual(
            restored.learner_id,
            learner.learner_id,
        )

        self.assertEqual(
            restored.display_name,
            learner.display_name,
        )

        self.assertFalse(
            restored.is_guest,
        )

    def test_missing_active_learner_does_not_restore(self):
        """No application state leaves the new Application without a learner."""

        application = Application(
            learner_repository=self.repository,
            application_state=self.application_state,
        )

        application.restore_active_learner()

        self.assertIsNone(
            application.active_learner,
        )

    def test_stale_active_learner_id_does_not_restore(self):
        """A stale learner ID does not create an invalid Active Learner."""

        self.application_state.save(
            {
                "active_learner_id": "missing-learner",
            }
        )

        application = Application(
            learner_repository=self.repository,
            application_state=self.application_state,
        )

        application.restore_active_learner()

        self.assertIsNone(
            application.active_learner,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
