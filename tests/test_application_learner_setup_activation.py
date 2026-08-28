"""Tests for Application learner setup result activation."""

from pathlib import Path
import sys
import unittest
from unittest.mock import Mock


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.application import Application
from core.learning.models.learner_setup_result import (
    LearnerSetupMode,
    LearnerSetupResult,
)


class TestApplicationLearnerSetupActivation(unittest.TestCase):
    """Test translation of setup results into Active Learners."""

    def _create_application(self):
        """Create an Application with an isolated learner repository."""
        application = Application()
        repository = Mock()
        application._learner_repository = repository
        return application, repository

    def test_named_setup_creates_and_activates_learner(self):
        """Named setup creates and activates a named LearnerIdentity."""
        application, repository = self._create_application()

        result = LearnerSetupResult(
            mode=LearnerSetupMode.NAMED,
            display_name="Budi",
        )

        learner = application.activate_learner_from_setup(result)

        self.assertIsNotNone(learner)
        self.assertEqual(learner.display_name, "Budi")
        self.assertFalse(learner.is_guest)
        self.assertTrue(learner.learner_id)
        self.assertIs(application.active_learner, learner)
        repository.save_learner.assert_called_once_with(learner)

    def test_guest_setup_creates_and_activates_guest(self):
        """Guest setup creates and activates the canonical Guest identity."""
        application, repository = self._create_application()

        result = LearnerSetupResult(
            mode=LearnerSetupMode.GUEST,
        )

        learner = application.activate_learner_from_setup(result)

        self.assertIsNotNone(learner)
        self.assertEqual(learner.display_name, "Guest")
        self.assertTrue(learner.is_guest)
        self.assertTrue(learner.learner_id)
        self.assertIs(application.active_learner, learner)
        repository.save_learner.assert_called_once_with(learner)

    def test_named_setup_generates_unique_learner_ids(self):
        """Separate named setup activations generate distinct learner IDs."""
        application, repository = self._create_application()

        result = LearnerSetupResult(
            mode=LearnerSetupMode.NAMED,
            display_name="Budi",
        )

        first = application.activate_learner_from_setup(result)
        second = application.activate_learner_from_setup(result)

        self.assertNotEqual(first.learner_id, second.learner_id)
        self.assertEqual(repository.save_learner.call_count, 2)

    def test_cancelled_setup_does_not_activate_learner(self):
        """Cancelled setup does not create or activate a learner."""
        application, repository = self._create_application()

        result = LearnerSetupResult(
            mode=LearnerSetupMode.CANCELLED,
        )

        learner = application.activate_learner_from_setup(result)

        self.assertIsNone(learner)
        self.assertIsNone(application.active_learner)
        repository.save_learner.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
