
import unittest


class TestCausalEvidenceVsEvidenceValidity(unittest.TestCase):

    def setUp(self):
        self.event_a = {
            "event_id": "event-A",
        }

        self.event_b = {
            "event_id": "event-B",
            "causes": ["event-A"],
            "causal_evidence": [
                {
                    "evidence_id": "evidence-1",
                    "validation_status": "unassessed",
                }
            ],
        }

    def test_01_causal_assertion_is_present(self):
        self.assertIn(
            self.event_a["event_id"],
            self.event_b["causes"],
        )

    def test_02_evidence_reference_is_present(self):
        self.assertEqual(
            len(self.event_b["causal_evidence"]),
            1,
        )
        self.assertEqual(
            self.event_b["causal_evidence"][0]["evidence_id"],
            "evidence-1",
        )

    def test_03_evidence_presence_does_not_mean_validated(self):
        evidence = self.event_b["causal_evidence"][0]

        self.assertEqual(
            evidence["validation_status"],
            "unassessed",
        )

    def test_04_evidence_reference_and_validation_status_are_distinct(self):
        evidence = self.event_b["causal_evidence"][0]

        self.assertIn("evidence_id", evidence)
        self.assertIn("validation_status", evidence)

    def test_05_validation_status_can_change_without_changing_event_identity(self):
        event_b_identity = self.event_b["event_id"]
        evidence = self.event_b["causal_evidence"][0]

        evidence["validation_status"] = "assessed"

        self.assertEqual(
            self.event_b["event_id"],
            event_b_identity,
        )
        self.assertEqual(
            evidence["evidence_id"],
            "evidence-1",
        )

    def test_06_evidence_validation_does_not_automatically_rewrite_causal_assertion(self):
        causes_before = list(self.event_b["causes"])

        self.event_b["causal_evidence"][0][
            "validation_status"
        ] = "rejected"

        self.assertEqual(
            self.event_b["causes"],
            causes_before,
        )


if __name__ == "__main__":
    unittest.main()
