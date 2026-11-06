
import unittest


class TestStep42_04CoexistingMembershipAndEndpointChanges(
    unittest.TestCase
):
    """
    Step 42-4
    Coexisting Membership and Endpoint Changes

    Research Question:
        Can Composition Membership and Relationship Endpoint
        Participation change together without their changes
        being semantically identical?

    Scope:
        Coexisting changes and semantic independence.

    Out of scope:
        Evaluation, Decision, Policy, Constraint,
        State, Lifecycle, and production implementation.
    """

    def setUp(self):
        self.composition_before = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        self.composition_after = {
            "identity": "composition-1",
            "members": ["context-A", "context-C"],
        }

        self.relationship_before = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.relationship_after = {
            "identity": "relationship-1",
            "source": "context-C",
            "target": "context-D",
        }

    def test_composition_membership_changes(self):
        self.assertNotEqual(
            self.composition_before["members"],
            self.composition_after["members"],
        )

    def test_relationship_endpoints_change(self):
        self.assertNotEqual(
            self.relationship_before["source"],
            self.relationship_after["source"],
        )
        self.assertNotEqual(
            self.relationship_before["target"],
            self.relationship_after["target"],
        )

    def test_both_changes_can_coexist(self):
        membership_changed = (
            self.composition_before["members"]
            != self.composition_after["members"]
        )

        endpoints_changed = (
            self.relationship_before["source"]
            != self.relationship_after["source"]
            or self.relationship_before["target"]
            != self.relationship_after["target"]
        )

        self.assertTrue(membership_changed)
        self.assertTrue(endpoints_changed)

    def test_membership_and_endpoint_values_are_not_identical(self):
        self.assertNotEqual(
            self.composition_after["members"],
            [
                self.relationship_after["source"],
                self.relationship_after["target"],
            ],
        )

    def test_composition_identity_can_remain_stable(self):
        self.assertEqual(
            self.composition_before["identity"],
            self.composition_after["identity"],
        )

    def test_relationship_identity_can_remain_stable(self):
        self.assertEqual(
            self.relationship_before["identity"],
            self.relationship_after["identity"],
        )


if __name__ == "__main__":
    unittest.main()
