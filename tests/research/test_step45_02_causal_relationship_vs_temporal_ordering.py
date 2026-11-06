
import unittest


class TestCausalRelationshipVsTemporalOrdering(unittest.TestCase):

    def setUp(self):
        self.event_a = {
            "event_id": "event-A",
            "causes": [],
        }

        self.event_b = {
            "event_id": "event-B",
            "causes": ["event-A"],
        }

    def test_01_events_have_distinct_identities(self):
        self.assertNotEqual(
            self.event_a["event_id"],
            self.event_b["event_id"],
        )

    def test_02_event_b_explicitly_references_event_a_as_cause(self):
        self.assertIn(
            self.event_a["event_id"],
            self.event_b["causes"],
        )

    def test_03_causal_reference_exists_without_sequence_fields(self):
        self.assertNotIn("sequence", self.event_a)
        self.assertNotIn("sequence", self.event_b)

    def test_04_causal_metadata_is_present(self):
        self.assertIn("causes", self.event_a)
        self.assertIn("causes", self.event_b)

    def test_05_causal_reference_does_not_require_ordering_attribute_in_fixture(self):
        self.assertEqual(self.event_b["causes"], ["event-A"])
        self.assertNotIn("sequence", self.event_a)
        self.assertNotIn("sequence", self.event_b)

    def test_06_causal_reference_and_ordering_are_distinct_representations(self):
        causal_reference = self.event_b["causes"]

        self.assertEqual(causal_reference, ["event-A"])
        self.assertFalse(
            "sequence" in self.event_a
            or "sequence" in self.event_b
        )


if __name__ == "__main__":
    unittest.main()
