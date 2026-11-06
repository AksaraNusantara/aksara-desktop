import unittest


class TestStep41_04ContextCompositionRelationshipCoexistence(
    unittest.TestCase
):
    """
    Step 41-4
    Context Composition + Relationship Coexistence

    Research Question:
        Apakah Context Composition dan Relationship dapat coexist
        tanpa semantic collapse atau identity fusion?

    Scope:
        Coexistence and semantic separation.

    Out of scope:
        Evaluation
        Decision
        Policy
        Constraint
        State
        Lifecycle
        Production implementation
    """

    def test_composition_and_relationship_can_coexist(self):
        composition = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
                "context-C",
            ],
        }

        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.assertIsNotNone(composition)
        self.assertIsNotNone(relationship)

    def test_composition_and_relationship_can_reference_same_contexts(self):
        composition = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
            ],
        }

        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.assertIn(
            relationship["source"],
            composition["members"],
        )

        self.assertIn(
            relationship["target"],
            composition["members"],
        )

    def test_composition_membership_does_not_become_relationship(self):
        composition = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
            ],
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

        self.assertEqual(
            composition["members"],
            [
                "context-A",
                "context-B",
            ],
        )

        self.assertEqual(
            relationship["source"],
            "context-A",
        )

        self.assertEqual(
            relationship["target"],
            "context-B",
        )

    def test_relationship_does_not_become_composition(self):
        composition = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
            ],
        }

        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.assertNotEqual(
            relationship,
            composition,
        )

        self.assertNotEqual(
            relationship["identity"],
            composition["identity"],
        )

    def test_relationship_can_change_without_changing_composition(self):
        composition = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
            ],
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

        self.assertEqual(
            composition["members"],
            [
                "context-A",
                "context-B",
            ],
        )

    def test_composition_can_change_without_changing_relationship(self):
        composition_before = {
            "identity": "composition-1",
            "members": [
                "context-A",
                "context-B",
            ],
        }

        composition_after = {
            "identity": "composition-2",
            "members": [
                "context-A",
                "context-B",
                "context-C",
            ],
        }

        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        self.assertNotEqual(
            composition_before["identity"],
            composition_after["identity"],
        )

        self.assertEqual(
            relationship["identity"],
            "relationship-1",
        )

        self.assertEqual(
            relationship["source"],
            "context-A",
        )

        self.assertEqual(
            relationship["target"],
            "context-B",
        )


if __name__ == "__main__":
    unittest.main()