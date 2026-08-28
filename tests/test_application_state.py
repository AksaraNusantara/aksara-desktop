"""Tests for persistent Application State."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.learning.storage.json_adapter import JSONAdapter


APPLICATION_STATE_KEY = "application_state"


class TestApplicationState(unittest.TestCase):
    """Test persistence of Application-owned state."""

    def setUp(self) -> None:
        """Create isolated temporary storage."""

        self.temp_dir = tempfile.TemporaryDirectory()

        self.storage = JSONAdapter(
            self.temp_dir.name,
        )

    def tearDown(self) -> None:
        """Remove temporary storage."""

        self.temp_dir.cleanup()

    def test_missing_active_learner_returns_none(self):
        """Missing application state has no active learner."""

        state = self.storage.load(
            APPLICATION_STATE_KEY,
        )

        self.assertIsNone(state)

    def test_active_learner_id_can_be_saved(self):
        """Application state can store an active learner ID."""

        state = {
            "active_learner_id": "learner-001",
        }

        self.storage.save(
            APPLICATION_STATE_KEY,
            state,
        )

        self.assertTrue(
            self.storage.exists(
                APPLICATION_STATE_KEY,
            )
        )

    def test_active_learner_id_can_be_loaded(self):
        """Stored active learner ID can be restored."""

        state = {
            "active_learner_id": "learner-001",
        }

        self.storage.save(
            APPLICATION_STATE_KEY,
            state,
        )

        loaded = self.storage.load(
            APPLICATION_STATE_KEY,
        )

        self.assertEqual(
            loaded,
            {
                "active_learner_id": "learner-001",
            },
        )

    def test_saving_new_active_learner_replaces_previous(self):
        """Saving a new active learner replaces the previous state."""

        self.storage.save(
            APPLICATION_STATE_KEY,
            {
                "active_learner_id": "learner-001",
            },
        )

        self.storage.save(
            APPLICATION_STATE_KEY,
            {
                "active_learner_id": "learner-002",
            },
        )

        loaded = self.storage.load(
            APPLICATION_STATE_KEY,
        )

        self.assertEqual(
            loaded,
            {
                "active_learner_id": "learner-002",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)