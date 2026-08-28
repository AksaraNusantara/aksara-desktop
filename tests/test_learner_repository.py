"""Contract tests for the dedicated LearnerRepository boundary."""

from pathlib import Path
import sys
import tempfile
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.learning.models.learner_identity import LearnerIdentity
from core.learning.repositories.learner_repository import (
    StorageLearnerRepository,
)
from core.learning.storage.json_adapter import JSONAdapter


class TestLearnerRepository(unittest.TestCase):
    """Validate ADR-0003 learner persistence semantics."""

    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = (
            Path(self._temp_dir.name) / "learners.json"
        )
        self.storage = JSONAdapter(self.storage_path)
        self.repository = StorageLearnerRepository(self.storage)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_named_learner_round_trip(self):
        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        self.repository.save_learner(learner)

        self.assertEqual(
            self.repository.load_learner("learner-001"),
            learner,
        )

    def test_guest_round_trip(self):
        learner = LearnerIdentity(
            learner_id="guest-001",
            display_name="Guest",
            is_guest=True,
        )

        self.repository.save_learner(learner)

        self.assertEqual(
            self.repository.load_learner("guest-001"),
            learner,
        )

    def test_multiple_learners_are_persisted(self):
        learners = [
            LearnerIdentity(
                learner_id="learner-001",
                display_name="Budi",
                is_guest=False,
            ),
            LearnerIdentity(
                learner_id="learner-002",
                display_name="Sari",
                is_guest=False,
            ),
            LearnerIdentity(
                learner_id="guest-001",
                display_name="Guest",
                is_guest=True,
            ),
        ]

        for learner in learners:
            self.repository.save_learner(learner)

        loaded = self.repository.load_learners()

        self.assertEqual(
            {learner.learner_id for learner in loaded},
            {"learner-001", "learner-002", "guest-001"},
        )

    def test_existing_learner_is_replaced(self):
        original = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )
        replacement = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi Updated",
            is_guest=False,
        )

        self.repository.save_learner(original)
        self.repository.save_learner(replacement)

        self.assertEqual(
            self.repository.load_learner("learner-001"),
            replacement,
        )

    def test_missing_learner_returns_none(self):
        self.assertIsNone(
            self.repository.load_learner("missing"),
        )

    def test_empty_store_returns_empty_list(self):
        self.assertEqual(
            self.repository.load_learners(),
            [],
        )

    def test_unicode_display_name_survives_round_trip(self):
        learner = LearnerIdentity(
            learner_id="learner-jawa",
            display_name="ꦧꦸꦢꦶ",
            is_guest=False,
        )

        self.repository.save_learner(learner)

        loaded = self.repository.load_learner("learner-jawa")

        self.assertEqual(
            loaded.display_name,
            "ꦧꦸꦢꦶ",
        )

    def test_repository_uses_dedicated_learners_key(self):
        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
            is_guest=False,
        )

        self.repository.save_learner(learner)

        stored = self.storage.load("learners")

        self.assertIsNotNone(stored)
        self.assertIn("learner-001", stored)


if __name__ == "__main__":
    unittest.main(verbosity=2)
