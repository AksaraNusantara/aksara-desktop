
import unittest


class TestStep43_03MembershipAdditionVsContextIdentityStability(
    unittest.TestCase
):
    """
    Step 43-3
    Membership Addition vs Context Identity Stability

    Research Question:
        Can a Context be added to a Composition while
        retaining its identity and existing memberships?

    Scope:
        Membership addition and identity stability.

    Out of scope:
        Evaluation, Decision, Policy, Constraint,
        State, Lifecycle, and production implementation.
    """

    def setUp(self):
        self.context_before = {
            "identity": "context-A",
        }

        self.context_after = {
            "identity": "context-A",
        }

        self.composition_1_before = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        self.composition_1_after = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        self.composition_2_before = {
            "identity": "composition-2",
            "members": ["context-C"],
        }

        self.composition_2_after = {
            "identity": "composition-2",
            "members": ["context-C", "context-A"],
        }

    def test_context_identity_remains_unchanged(self):
        self.assertEqual(
            self.context_before["identity"],
            self.context_after["identity"],
        )

    def test_membership_is_added_to_second_composition(self):
        self.assertNotIn(
            "context-A",
            self.composition_2_before["members"],
        )

        self.assertIn(
            "context-A",
            self.composition_2_after["members"],
        )

    def test_existing_membership_remains_unchanged(self):
        self.assertEqual(
            self.composition_1_before["members"],
            self.composition_1_after["members"],
        )

    def test_addition_does_not_require_context_identity_change(self):
        self.assertIn(
            "context-A",
            self.composition_2_after["members"],
        )

        self.assertEqual(
            self.context_before["identity"],
            self.context_after["identity"],
        )

    def test_addition_does_not_require_other_membership_change(self):
        self.assertIn(
            "context-A",
            self.composition_2_after["members"],
        )

        self.assertEqual(
            self.composition_1_before,
            self.composition_1_after,
        )

    def test_composition_identities_remain_distinct(self):
        self.assertNotEqual(
            self.composition_1_after["identity"],
            self.composition_2_after["identity"],
        )


if __name__ == "__main__":
    unittest.main()
