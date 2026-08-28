"""Tests for Active Learner integration during Application bootstrap."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from application.application import Application


class TestApplicationBootstrapLearner(unittest.TestCase):
    """Test Active Learner bootstrap integration."""

    def test_application_has_no_active_learner_before_initialization(self):
        """Application starts without an Active Learner."""

        application = Application()

        self.assertIsNone(
            application.active_learner,
        )

    def test_initialize_restores_active_learner(self):
        """Application initialization attempts to restore Active Learner."""

        application = Application()

        with patch.object(
            application,
            "restore_active_learner",
        ) as restore_mock:

            # Prevent the real Qt/MainWindow bootstrap from being
            # part of this contract test.
            with patch.object(
                application._engine,
                "initialize",
            ), patch.object(
                application._engine,
                "list",
                return_value=[],
            ), patch(
                "application.application.MainWindow",
            ):

                application.initialize()

        restore_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)