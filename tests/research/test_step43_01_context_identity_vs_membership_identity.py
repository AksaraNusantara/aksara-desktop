
import unittest


class TestStep43_01ContextIdentityVsMembershipIdentity(
    unittest.TestCase
):
    """
    Step 43-1
    Context Identity vs Membership Identity

    Research Question:
        Can Context Identity and Composition Membership
        Identity be distinguished semantically?

    Scope:
        Context identity and membership identity.

    Out of scope:
        Evaluation, Decision, Policy, Constraint,
        State, Lifecycle, and production implementation.
    """

    def setUp(self):
        self.context = {
            "identity": "context-A",
        }

        self.composition_1 = {
            "identity": "composition-1",
            "members": ["context-A"],
        }

        self.composition_2 = {
            "identity": "composition-2",
            "members": ["context-A"],
        }

        self.membership_1 = {
            "context": "context-A",
            "composition": "composition-1",
        }

        self.membership_2 = {
            "context": "context-A",
            "composition": "composition-2",
        }

    def test_context_identity_is_explicit(self):
        self.assertEqual(
            self.context["identity"],
            "context-A",
        )

    def test_same_context_can_belong_to_two_compositions(self):
        self.assertIn(
            self.context["identity"],
            self.composition_1["members"],
        )

        self.assertIn(
            self.context["identity"],
            self.composition_2["members"],
        )

    def test_composition_identities_are_distinct(self):
        self.assertNotEqual(
            self.composition_1["identity"],
            self.composition_2["identity"],
        )

    def test_memberships_can_be_distinguished_by_composition(self):
        self.assertEqual(
            self.membership_1["context"],
            self.membership_2["context"],
        )

        self.assertNotEqual(
            self.membership_1["composition"],
            self.membership_2["composition"],
        )

    def test_membership_records_are_distinct(self):
        self.assertNotEqual(
            self.membership_1,
            self.membership_2,
        )

    def test_membership_identity_is_not_context_identity(self):
        self.assertNotEqual(
            self.context["identity"],
            self.membership_1,
        )

        self.assertNotEqual(
            self.context["identity"],
            self.membership_2,
        )


if __name__ == "__main__":
    unittest.main()
