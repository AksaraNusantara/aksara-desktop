"""Tests for Application-level Active Learner behavior."""

from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from application.application import Application
from core.learning.models.learner_identity import LearnerIdentity


class FakeLearnerRepository:
    """Minimal repository double for Application tests."""

    def __init__(self) -> None:
        self.saved_learners: list[LearnerIdentity] = []

    def save_learner(
        self,
        learner: LearnerIdentity,
    ) -> None:
        self.saved_learners.append(learner)

    def load_learner(
        self,
        learner_id: str,
    ) -> LearnerIdentity | None:
        for learner in self.saved_learners:
            if learner.learner_id == learner_id:
                return learner

        return None


class FakeApplicationState:
    """Minimal application-state double."""

    def __init__(self) -> None:
        self._state = None

    def save(self, state: dict) -> None:
        self._state = state.copy()

    def load(self) -> dict | None:
        if self._state is None:
            return None

        return self._state.copy()


class TestApplicationLearner(unittest.TestCase):
    """Test Application Active Learner behavior."""

    def setUp(self) -> None:
        """Create an Application with controlled dependencies."""

        self.repository = FakeLearnerRepository()
        self.application_state = FakeApplicationState()

        self.application = Application(
            learner_repository=self.repository,
            application_state=self.application_state,
        )

    def test_initial_active_learner_is_none(self):
        """Application starts without an Active Learner."""

        self.assertIsNone(
            self.application.active_learner,
        )

    def test_named_learner_becomes_active(self):
        """A named LearnerIdentity becomes the Active Learner."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Supriyanto",
            is_guest=False,
        )

        self.application.set_active_learner(
            learner,
        )

        self.assertIs(
            self.application.active_learner,
            learner,
        )

    def test_guest_becomes_active(self):
        """A Guest LearnerIdentity becomes the Active Learner."""

        learner = LearnerIdentity(
            learner_id="guest-001",
            display_name="Guest",
            is_guest=True,
        )

        self.application.set_active_learner(
            learner,
        )

        self.assertIs(
            self.application.active_learner,
            learner,
        )

    def test_active_learner_is_persisted(self):
        """Setting the Active Learner persists it."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Supriyanto",
            is_guest=False,
        )

        self.application.set_active_learner(
            learner,
        )

        self.assertEqual(
            self.repository.saved_learners,
            [learner],
        )

    def test_restore_active_learner(self):
        """Application restores the persisted Active Learner."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Supriyanto",
            is_guest=False,
        )

        self.repository.save_learner(learner)

        self.application_state.save(
            {
                "active_learner_id": "learner-001",
            },
        )

        self.application.restore_active_learner()

        self.assertIs(
            self.application.active_learner,
            learner,
        )

    def test_restore_without_application_state(self):
        """No persisted state leaves Active Learner unset."""

        self.application.restore_active_learner()

        self.assertIsNone(
            self.application.active_learner,
        )

    def test_restore_missing_learner(self):
        """A stale learner ID does not create an invalid Active Learner."""

        self.application_state.save(
            {
                "active_learner_id": "missing-learner",
            },
        )

        self.application.restore_active_learner()

        self.assertIsNone(
            self.application.active_learner,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
