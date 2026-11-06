import unittest


class TestOccurrenceIdentityVsSecondaryOrdering(unittest.TestCase):

    def setUp(self):
        self.occurrence_a = {
            "occurrence_id": "occurrence-A",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 10,
            "tie_breaker": 1,
        }

        self.occurrence_b = {
            "occurrence_id": "occurrence-B",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 10,
            "tie_breaker": 2,
        }

    def test_01_primary_ordering_values_are_equal(self):
        self.assertEqual(
            self.occurrence_a["sequence"],
            self.occurrence_b["sequence"],
        )

    def test_02_secondary_ordering_values_are_distinct(self):
        self.assertNotEqual(
            self.occurrence_a["tie_breaker"],
            self.occurrence_b["tie_breaker"],
        )

    def test_03_secondary_criterion_can_order_occurrences(self):
        ordered = sorted(
            [self.occurrence_b, self.occurrence_a],
            key=lambda occurrence: (
                occurrence["sequence"],
                occurrence["tie_breaker"],
            ),
        )

        self.assertEqual(
            [item["occurrence_id"] for item in ordered],
            ["occurrence-A", "occurrence-B"],
        )

    def test_04_ordering_does_not_change_occurrence_identity(self):
        original_ids = {
            self.occurrence_a["occurrence_id"],
            self.occurrence_b["occurrence_id"],
        }

        ordered = sorted(
            [self.occurrence_b, self.occurrence_a],
            key=lambda occurrence: (
                occurrence["sequence"],
                occurrence["tie_breaker"],
            ),
        )

        ordered_ids = {
            item["occurrence_id"] for item in ordered
        }

        self.assertEqual(original_ids, ordered_ids)

    def test_05_ordering_does_not_change_membership_endpoints(self):
        for occurrence in (self.occurrence_a, self.occurrence_b):
            self.assertEqual(occurrence["context_id"], "context-A")
            self.assertEqual(
                occurrence["composition_id"],
                "composition-X",
            )

    def test_06_secondary_ordering_is_not_occurrence_identity(self):
        identity_before = self.occurrence_a["occurrence_id"]

        self.occurrence_a["tie_breaker"] = 99

        self.assertEqual(
            self.occurrence_a["occurrence_id"],
            identity_before,
        )


if __name__ == "__main__":
    unittest.main()