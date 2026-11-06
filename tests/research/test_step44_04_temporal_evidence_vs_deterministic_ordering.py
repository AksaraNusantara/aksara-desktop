import unittest


class TestTemporalEvidenceVsDeterministicOrdering(unittest.TestCase):

    def setUp(self):
        self.occurrence_a = {
            "occurrence_id": "occurrence-A",
            "sequence": 10,
            "tie_breaker": 1,
            "occurred_at": None,
        }

        self.occurrence_b = {
            "occurrence_id": "occurrence-B",
            "sequence": 10,
            "tie_breaker": 2,
            "occurred_at": None,
        }

    def test_01_tie_breaker_can_produce_deterministic_order(self):
        ordered = sorted(
            [self.occurrence_b, self.occurrence_a],
            key=lambda item: (
                item["sequence"],
                item["tie_breaker"],
            ),
        )

        self.assertEqual(
            [item["occurrence_id"] for item in ordered],
            ["occurrence-A", "occurrence-B"],
        )

    def test_02_deterministic_order_does_not_supply_time_evidence(self):
        self.assertIsNone(self.occurrence_a["occurred_at"])
        self.assertIsNone(self.occurrence_b["occurred_at"])

    def test_03_tie_breaker_alone_does_not_establish_temporal_precedence(self):
        self.assertLess(
            self.occurrence_a["tie_breaker"],
            self.occurrence_b["tie_breaker"],
        )

        self.assertIsNone(self.occurrence_a["occurred_at"])
        self.assertIsNone(self.occurrence_b["occurred_at"])

    def test_04_occurrence_identity_exists_without_timestamp(self):
        self.assertTrue(self.occurrence_a["occurrence_id"])
        self.assertTrue(self.occurrence_b["occurrence_id"])

    def test_05_missing_time_evidence_does_not_merge_occurrences(self):
        self.assertNotEqual(
            self.occurrence_a["occurrence_id"],
            self.occurrence_b["occurrence_id"],
        )

    def test_06_ordering_policy_and_time_evidence_are_separate_fields(self):
        for occurrence in (self.occurrence_a, self.occurrence_b):
            self.assertIn("tie_breaker", occurrence)
            self.assertIn("occurred_at", occurrence)

        self.assertIsNone(self.occurrence_a["occurred_at"])
        self.assertIsNone(self.occurrence_b["occurred_at"])


if __name__ == "__main__":
    unittest.main()