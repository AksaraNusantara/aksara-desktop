"""Tests for Application learner setup orchestration."""

from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from application.application import Application
from core.learning.models.learner_setup_result import (
    LearnerSetupMode,
    LearnerSetupResult,
)


class FakeLearnerSetupDialog:
    """Test double for the learner setup dialog."""

    result_value = LearnerSetupResult(
        mode=LearnerSetupMode.NAMED,
        display_name="Budi",
    )

    def __init__(self, parent=None):
        """Initialize the fake learner setup dialog."""
        self.parent = parent
        self.exec_called = False

    def exec(self):
        """Simulate an accepted setup dialog."""
        self.exec_called = True
        return 1

    def result(self):
        """Return the configured learner setup result."""
        return self.result_value


class TestApplicationLearnerSetup(unittest.TestCase):
    """Test Application learner setup orchestration."""

    def _create_application(self):
        """Create an Application using its production constructor."""
        return Application()

    def test_existing_active_learner_does_not_open_setup(self):
        """Existing Active Learner bypasses the setup dialog."""
        application = self._create_application()
        existing_learner = Mock()

        application._active_learner = existing_learner

        with patch(
            "application.application.LearnerSetupDialog",
            create=True,
        ) as dialog_class:
            application._ensure_active_learner()

        dialog_class.assert_not_called()

        self.assertIs(
            application.active_learner,
            existing_learner,
        )

    def test_missing_active_learner_opens_setup(self):
        """Missing Active Learner opens setup and consumes its result."""
        application = self._create_application()

        with patch(
            "application.application.LearnerSetupDialog",
            FakeLearnerSetupDialog,
            create=True,
        ):
            with patch.object(
                application,
                "activate_learner_from_setup",
            ) as activate_mock:
                activate_mock.return_value = Mock()

                application._ensure_active_learner()

        activate_mock.assert_called_once_with(
            FakeLearnerSetupDialog.result_value,
        )

    def test_setup_activation_is_delegated_to_application(self):
        """Setup flow delegates learner activation to Application."""
        application = self._create_application()
        learner = Mock()

        with patch(
            "application.application.LearnerSetupDialog",
            FakeLearnerSetupDialog,
            create=True,
        ):
            with patch.object(
                application,
                "activate_learner_from_setup",
                return_value=learner,
            ) as activate_mock:
                application._ensure_active_learner()

        activate_mock.assert_called_once_with(
            FakeLearnerSetupDialog.result_value,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
