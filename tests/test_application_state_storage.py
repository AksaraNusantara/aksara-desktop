"""Tests for ApplicationStateStorage."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from application.application_state import ApplicationStateStorage
from core.learning.storage.json_adapter import JSONAdapter


class TestApplicationStateStorage(unittest.TestCase):
    """Test Application-owned state persistence."""

    def setUp(self) -> None:
        """Create isolated storage."""

        self.temp_dir = tempfile.TemporaryDirectory()

        storage = JSONAdapter(
            self.temp_dir.name,
        )

        self.application_state = ApplicationStateStorage(
            storage,
        )

    def tearDown(self) -> None:
        """Remove isolated storage."""

        self.temp_dir.cleanup()

    def test_missing_state_returns_none(self):
        """Missing application state returns None."""

        self.assertIsNone(
            self.application_state.load()
        )

    def test_save_state(self):
        """Application state can be saved."""

        state = {
            "active_learner_id": "learner-001",
        }

        self.application_state.save(state)

        self.assertIsNotNone(
            self.application_state.load()
        )

    def test_load_state(self):
        """Saved application state can be loaded."""

        state = {
            "active_learner_id": "learner-001",
        }

        self.application_state.save(state)

        loaded = self.application_state.load()

        self.assertEqual(
            loaded,
            state,
        )

    def test_replace_state(self):
        """Saving new state replaces previous state."""

        self.application_state.save(
            {
                "active_learner_id": "learner-001",
            }
        )

        self.application_state.save(
            {
                "active_learner_id": "learner-002",
            }
        )

        loaded = self.application_state.load()

        self.assertEqual(
            loaded,
            {
                "active_learner_id": "learner-002",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)