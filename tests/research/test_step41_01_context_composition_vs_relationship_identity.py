import unittest


class TestStep41_01ContextCompositionVsRelationshipIdentity(
    unittest.TestCase
):
    """
    Step 41-1
    Context Composition vs Relationship Identity Boundary

    Research Question:
        Apakah Context Composition Identity dan Relationship Identity
        merupakan semantic identity yang berbeda?

    Scope:
        Identity boundary only.

    Out of scope:
        Evaluation
        Decision
        Policy
        Constraint
        State
        Lifecycle
        Production implementation
    """

    def test_context_identity_differs_from_composition_identity(self):
        context_a = "context-A"
        composition = {
            "identity": "composition-1",
            "members": [context_a],
        }

        self.assertNotEqual(
            context_a,
            composition["identity"],
        )

    def test_context_identity_differs_from_relationship_identity(self):
        context_a = "context-A"
        relationship = {
            "identity": "relationship-1",
            "source": context_a,
            "target": "context-B",
        }

        self.assertNotEqual(
            context_a,
            relationship["identity"],
        )

    def test_composition_identity_differs_from_relationship_identity(self):
        composition = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.assertNotEqual(
            composition["identity"],
            relationship["identity"],
        )

    def test_same_contexts_can_participate_in_distinct_composition_and_relationship(self):
        context_a = "context-A"
        context_b = "context-B"

        composition = {
            "identity": "composition-1",
            "members": [context_a, context_b],
        }

        relationship = {
            "identity": "relationship-1",
            "source": context_a,
            "target": context_b,
        }

        self.assertEqual(
            composition["members"],
            [context_a, context_b],
        )

        self.assertEqual(
            relationship["source"],
            context_a,
        )

        self.assertEqual(
            relationship["target"],
            context_b,
        )

        self.assertNotEqual(
            composition["identity"],
            relationship["identity"],
        )

    def test_relationship_identity_can_remain_distinct_when_composition_changes(self):
        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        composition_before = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        composition_after = {
            "identity": "composition-2",
            "members": ["context-A", "context-B", "context-C"],
        }

        self.assertNotEqual(
            composition_before["identity"],
            composition_after["identity"],
        )

        self.assertEqual(
            relationship["identity"],
            "relationship-1",
        )

    def test_composition_identity_can_remain_distinct_when_relationship_changes(self):
        composition = {
            "identity": "composition-1",
            "members": ["context-A", "context-B"],
        }

        relationship_before = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        relationship_after = {
            "identity": "relationship-2",
            "source": "context-A",
            "target": "context-C",
        }

        self.assertNotEqual(
            relationship_before["identity"],
            relationship_after["identity"],
        )

        self.assertEqual(
            composition["identity"],
            "composition-1",
        )


if __name__ == "__main__":
    unittest.main()