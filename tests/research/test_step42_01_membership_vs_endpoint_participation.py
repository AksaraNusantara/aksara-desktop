
import unittest


class TestStep42_01MembershipVsEndpointParticipation(
    unittest.TestCase
):
    """
    Step 42-1
    Composition Membership vs Relationship Endpoint Participation

    Research Question:
        Apakah Composition Membership dan Relationship Endpoint
        Participation dapat dibedakan secara semantic?

    Scope:
        Membership and endpoint participation only.

    Out of scope:
        Evaluation, Decision, Policy, Constraint,
        State, Lifecycle, and production implementation.
    """

    def setUp(self):
        self.composition = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        self.relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-C",
        }

    def test_composition_membership_is_explicit(self):
        self.assertIn(
            "context-A",
            self.composition["members"],
        )
        self.assertIn(
            "context-B",
            self.composition["members"],
        )

    def test_relationship_endpoints_are_explicit(self):
        self.assertEqual(
            self.relationship["source"],
            "context-A",
        )
        self.assertEqual(
            self.relationship["target"],
            "context-C",
        )

    def test_membership_does_not_imply_endpoint_participation(self):
        self.assertIn(
            "context-B",
            self.composition["members"],
        )

        self.assertNotIn(
            "context-B",
            [
                self.relationship["source"],
                self.relationship["target"],
            ],
        )

    def test_endpoint_participation_does_not_imply_membership(self):
        self.assertEqual(
            self.relationship["target"],
            "context-C",
        )

        self.assertNotIn(
            "context-C",
            self.composition["members"],
        )

    def test_membership_does_not_determine_relationship_direction(self):
        self.assertIn(
            "context-A",
            self.composition["members"],
        )

        self.assertEqual(
            self.relationship["source"],
            "context-A",
        )

        self.assertNotEqual(
            self.relationship["source"],
            self.relationship["target"],
        )

    def test_membership_and_endpoint_roles_can_coexist(self):
        shared_context = "context-A"

        self.assertIn(
            shared_context,
            self.composition["members"],
        )

        self.assertIn(
            shared_context,
            [
                self.relationship["source"],
                self.relationship["target"],
            ],
        )

        self.assertNotEqual(
            self.composition["identity"],
            self.relationship["identity"],
        )


if __name__ == "__main__":
    unittest.main()
