import unittest


class TestMembershipOccurrenceIdentityVsTemporalOrdering(unittest.TestCase):

    def setUp(self):
        # Two separate occurrences of the same Context–Composition
        # membership, separated by a removal and a later re-addition.
        self.occurrence_a = {
            "occurrence_id": "occurrence-A",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 1,
        }

        self.occurrence_b = {
            "occurrence_id": "occurrence-B",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 2,
        }

        self.occurrences = [
            self.occurrence_a,
            self.occurrence_b,
        ]

    def test_01_separate_occurrences_have_distinct_identities(self):
        self.assertNotEqual(
            self.occurrence_a["occurrence_id"],
            self.occurrence_b["occurrence_id"],
        )

    def test_02_occurrences_can_share_the_same_membership_endpoints(self):
        self.assertEqual(
            self.occurrence_a["context_id"],
            self.occurrence_b["context_id"],
        )
        self.assertEqual(
            self.occurrence_a["composition_id"],
            self.occurrence_b["composition_id"],
        )

    def test_03_occurrences_have_distinct_temporal_order_values(self):
        self.assertNotEqual(
            self.occurrence_a["sequence"],
            self.occurrence_b["sequence"],
        )

    def test_04_temporal_order_does_not_replace_occurrence_identity(self):
        by_sequence = sorted(
            self.occurrences,
            key=lambda occurrence: occurrence["sequence"],
        )

        self.assertEqual(
            by_sequence[0]["occurrence_id"],
            "occurrence-A",
        )
        self.assertEqual(
            by_sequence[1]["occurrence_id"],
            "occurrence-B",
        )

    def test_05_changing_order_value_preserves_occurrence_identity(self):
        changed_occurrence = dict(self.occurrence_a)
        changed_occurrence["sequence"] = 99

        self.assertEqual(
            changed_occurrence["occurrence_id"],
            self.occurrence_a["occurrence_id"],
        )
        self.assertEqual(
            changed_occurrence["context_id"],
            self.occurrence_a["context_id"],
        )
        self.assertEqual(
            changed_occurrence["composition_id"],
            self.occurrence_a["composition_id"],
        )

    def test_06_reordering_collection_preserves_occurrence_identities(self):
        reordered = list(reversed(self.occurrences))

        original_ids = {
            occurrence["occurrence_id"]
            for occurrence in self.occurrences
        }
        reordered_ids = {
            occurrence["occurrence_id"]
            for occurrence in reordered
        }

        self.assertEqual(original_ids, reordered_ids)


if __name__ == "__main__":
    unittest.main()