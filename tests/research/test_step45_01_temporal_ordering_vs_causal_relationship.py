
import unittest


class TestTemporalOrderingVsCausalRelationship(unittest.TestCase):

    def setUp(self):
        # Two events with an explicit temporal order.
        # No causal relationship is asserted by this fixture.
        self.event_a = {
            "event_id": "event-A",
            "sequence": 1,
            "causes": [],
        }

        self.event_b = {
            "event_id": "event-B",
            "sequence": 2,
            "causes": [],
        }

    def test_01_events_have_distinct_identities(self):
        self.assertNotEqual(
            self.event_a["event_id"],
            self.event_b["event_id"],
        )

    def test_02_events_have_distinct_temporal_order_values(self):
        self.assertNotEqual(
            self.event_a["sequence"],
            self.event_b["sequence"],
        )

    def test_03_event_a_precedes_event_b_in_the_defined_order(self):
        self.assertLess(
            self.event_a["sequence"],
            self.event_b["sequence"],
        )

    def test_04_temporal_order_does_not_encode_a_causal_link(self):
        self.assertNotIn(
            self.event_a["event_id"],
            self.event_b["causes"],
        )

    def test_05_causal_metadata_is_separate_from_sequence(self):
        self.assertIn("sequence", self.event_a)
        self.assertIn("causes", self.event_a)
        self.assertIn("sequence", self.event_b)
        self.assertIn("causes", self.event_b)

    def test_06_temporal_order_can_exist_without_asserted_causality(self):
        self.assertLess(
            self.event_a["sequence"],
            self.event_b["sequence"],
        )
        self.assertEqual(self.event_b["causes"], [])


if __name__ == "__main__":
    unittest.main()
