import unittest


class TestOccurrenceIdentityVsEqualTemporalOrder(unittest.TestCase):

    def setUp(self):
        self.occurrence_a = {
            "occurrence_id": "occurrence-A",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 10,
        }

        self.occurrence_b = {
            "occurrence_id": "occurrence-B",
            "context_id": "context-A",
            "composition_id": "composition-X",
            "sequence": 10,
        }

    def test_01_occurrences_have_distinct_identities(self):
        self.assertNotEqual(
            self.occurrence_a["occurrence_id"],
            self.occurrence_b["occurrence_id"],
        )

    def test_02_occurrences_can_share_the_same_sequence_value(self):
        self.assertEqual(
            self.occurrence_a["sequence"],
            self.occurrence_b["sequence"],
        )

    def test_03_equal_sequence_does_not_collapse_occurrence_identity(self):
        self.assertNotEqual(
            self.occurrence_a["occurrence_id"],
            self.occurrence_b["occurrence_id"],
        )

    def test_04_occurrences_can_share_the_same_membership_endpoints(self):
        self.assertEqual(
            self.occurrence_a["context_id"],
            self.occurrence_b["context_id"],
        )
        self.assertEqual(
            self.occurrence_a["composition_id"],
            self.occurrence_b["composition_id"],
        )

    def test_05_occurrence_identity_is_not_derived_from_sequence_alone(self):
        identity_a = self.occurrence_a["occurrence_id"]
        identity_b = self.occurrence_b["occurrence_id"]

        self.assertNotEqual(identity_a, identity_b)
        self.assertEqual(
            self.occurrence_a["sequence"],
            self.occurrence_b["sequence"],
        )

    def test_06_equal_sequence_does_not_establish_total_order(self):
        self.assertEqual(
            self.occurrence_a["sequence"],
            self.occurrence_b["sequence"],
        )

        # The shared sequence value alone cannot establish which
        # occurrence precedes the other.
        self.assertFalse(
            self.occurrence_a["sequence"]
            < self.occurrence_b["sequence"]
        )
        self.assertFalse(
            self.occurrence_b["sequence"]
            < self.occurrence_a["sequence"]
        )


if __name__ == "__main__":
    unittest.main()