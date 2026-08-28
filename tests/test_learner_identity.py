"""
Tests for the LearnerIdentity domain model.

Architecture reference:
    ADR-0003 — Learner Identity and Guest Mode
"""


import sys
import unittest
from pathlib import Path


# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from core.learning.models.learner_identity import LearnerIdentity


class TestLearnerIdentity(unittest.TestCase):
    """Test LearnerIdentity domain invariants."""

    def test_named_learner_is_valid(self):
        """A named learner creates a valid identity."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
        )

        self.assertEqual(
            learner.learner_id,
            "learner-001",
        )

        self.assertEqual(
            learner.display_name,
            "Budi",
        )

        self.assertFalse(
            learner.is_guest,
        )

    def test_guest_learner_is_valid(self):
        """Guest is represented as a valid learner identity."""

        learner = LearnerIdentity(
            learner_id="guest-001",
            display_name="Guest",
            is_guest=True,
        )

        self.assertEqual(
            learner.learner_id,
            "guest-001",
        )

        self.assertEqual(
            learner.display_name,
            "Guest",
        )

        self.assertTrue(
            learner.is_guest,
        )

    def test_empty_learner_id_is_rejected(self):
        """Learner ID must not be empty."""

        with self.assertRaisesRegex(
            ValueError,
            "learner_id cannot be empty.",
        ):
            LearnerIdentity(
                learner_id="",
                display_name="Budi",
            )

    def test_empty_display_name_is_rejected(self):
        """Display name must not be empty."""

        with self.assertRaisesRegex(
            ValueError,
            "display_name cannot be empty.",
        ):
            LearnerIdentity(
                learner_id="learner-001",
                display_name="",
            )

    def test_guest_must_use_guest_display_name(self):
        """Guest mode must use the canonical Guest display name."""

        with self.assertRaisesRegex(
            ValueError,
            'Guest learner must use display_name "Guest".',
        ):
            LearnerIdentity(
                learner_id="guest-001",
                display_name="Anonymous",
                is_guest=True,
            )

    def test_named_learner_may_use_guest_as_display_name(self):
        """
        A non-Guest learner is not constrained by the Guest mode flag.
        """

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Guest",
            is_guest=False,
        )

        self.assertEqual(
            learner.display_name,
            "Guest",
        )

        self.assertFalse(
            learner.is_guest,
        )

    def test_identity_is_immutable(self):
        """LearnerIdentity is immutable after creation."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
        )

        with self.assertRaises(AttributeError):
            learner.display_name = "Andi"

    def test_learner_id_is_independent_from_display_name(self):
        """Changing display name does not define learner identity."""

        learner = LearnerIdentity(
            learner_id="learner-001",
            display_name="Budi",
        )

        self.assertNotEqual(
            learner.learner_id,
            learner.display_name,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
