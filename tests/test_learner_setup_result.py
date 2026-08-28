"""Tests for LearnerSetupResult."""

from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.learning.models.learner_setup_result import (
    LearnerSetupMode,
    LearnerSetupResult,
)


class TestLearnerSetupResult(unittest.TestCase):
    """Test learner setup result contract."""

    def test_named_result_contains_display_name(self):
        """Named learner result carries the entered display name."""

        result = LearnerSetupResult(
            mode=LearnerSetupMode.NAMED,
            display_name="Budi",
        )

        self.assertEqual(
            result.mode,
            LearnerSetupMode.NAMED,
        )

        self.assertEqual(
            result.display_name,
            "Budi",
        )

    def test_guest_result_has_no_display_name(self):
        """Guest result does not carry a named learner."""

        result = LearnerSetupResult(
            mode=LearnerSetupMode.GUEST,
        )

        self.assertEqual(
            result.mode,
            LearnerSetupMode.GUEST,
        )

        self.assertIsNone(
            result.display_name,
        )

    def test_cancelled_result_has_no_display_name(self):
        """Cancelled setup does not produce a learner name."""

        result = LearnerSetupResult(
            mode=LearnerSetupMode.CANCELLED,
        )

        self.assertEqual(
            result.mode,
            LearnerSetupMode.CANCELLED,
        )

        self.assertIsNone(
            result.display_name,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
