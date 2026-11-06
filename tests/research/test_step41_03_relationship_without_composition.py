import unittest


class TestStep41_03RelationshipWithoutComposition(unittest.TestCase):
    """
    Step 41-3
    Relationship Without Context Composition

    Research Question:
        Apakah Relationship antar Context dapat eksis tanpa
        Context Composition?

    Scope:
        Relationship vs Composition existence.

    Out of scope:
        Evaluation
        Decision
        Policy
        Constraint
        State
        Lifecycle
        Production implementation
    """

    def test_relationship_can_exist_without_composition(self):
        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        composition = None

        self.assertIsNotNone(relationship)
        self.assertIsNone(composition)

    def test_relationship_does_not_require_composition_membership(self):
        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        composition_members = []

        self.assertEqual(
            relationship["source"],
            "context-A",
        )

        self.assertEqual(
            relationship["target"],
            "context-B",
        )

        self.assertEqual(
            composition_members,
            [],
        )

    def test_relationship_identity_can_exist_without_composition_identity(self):
        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        composition = None

        self.assertIsNotNone(
            relationship["identity"],
        )

        self.assertIsNone(composition)

    def test_multiple_relationships_can_exist_without_composition(self):
        relationships = [
            {
                "identity": "relationship-1",
                "source": "context-A",
                "target": "context-B",
            },
            {
                "identity": "relationship-2",
                "source": "context-B",
                "target": "context-C",
            },
        ]

        composition = None

        self.assertEqual(
            len(relationships),
            2,
        )

        self.assertIsNone(composition)

    def test_relationship_count_does_not_imply_composition(self):
        relationships = [
            {
                "identity": "relationship-1",
                "source": "context-A",
                "target": "context-B",
            },
            {
                "identity": "relationship-2",
                "source": "context-A",
                "target": "context-C",
            },
            {
                "identity": "relationship-3",
                "source": "context-B",
                "target": "context-C",
            },
        ]

        composition = None

        self.assertEqual(
            len(relationships),
            3,
        )

        self.assertIsNone(composition)

    def test_relationship_semantics_remain_distinct_without_composition(self):
        relationship = {
            "identity": "relationship-1",
            "source": "context-A",
            "target": "context-B",
        }

        composition = None

        self.assertEqual(
            relationship["source"],
            "context-A",
        )

        self.assertEqual(
            relationship["target"],
            "context-B",
        )

        self.assertIsNone(composition)


if __name__ == "__main__":
    unittest.main()