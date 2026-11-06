
import unittest


class TestCausalRelationshipVsCausalEvidence(unittest.TestCase):

    def setUp(self):
        self.event_a = {
            "event_id": "event-A",
        }

        self.event_b = {
            "event_id": "event-B",
            "causes": ["event-A"],
            "causal_evidence": [],
        }

    def test_01_events_have_distinct_identities(self):
        self.assertNotEqual(
            self.event_a["event_id"],
            self.event_b["event_id"],
        )

    def test_02_causal_relationship_is_explicitly_asserted(self):
        self.assertIn(
            self.event_a["event_id"],
            self.event_b["causes"],
        )

    def test_03_causal_evidence_is_represented_separately(self):
        self.assertIn("causes", self.event_b)
        self.assertIn("causal_evidence", self.event_b)

    def test_04_causal_assertion_can_exist_without_evidence_entries(self):
        self.assertIn(
            self.event_a["event_id"],
            self.event_b["causes"],
        )
        self.assertEqual(
            self.event_b["causal_evidence"],
            [],
        )

    def test_05_missing_evidence_entries_do_not_remove_the_assertion(self):
        self.assertEqual(
            self.event_b["causes"],
            ["event-A"],
        )
        self.assertEqual(
            self.event_b["causal_evidence"],
            [],
        )

    def test_06_evidence_metadata_does_not_define_event_identity(self):
        event_b_identity = self.event_b["event_id"]

        self.event_b["causal_evidence"].append(
            "evidence-reference-1"
        )

        self.assertEqual(
            self.event_b["event_id"],
            event_b_identity,
        )
        self.assertIn(
            "event-A",
            self.event_b["causes"],
        )


if __name__ == "__main__":
    unittest.main()
