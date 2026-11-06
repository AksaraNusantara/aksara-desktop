
import unittest


class TestEvidenceStatusVsClaimReassessmentTrigger(unittest.TestCase):

    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "claim_status": "recorded",
        }

        self.evidence = {
            "evidence_id": "evidence-1",
            "claim_id": "claim-1",
            "validation_status": "unassessed",
        }

        self.reassessment = {
            "claim_id": "claim-1",
            "triggered": False,
            "reason": None,
        }

    def test_01_evidence_status_can_change_without_triggering_reassessment(self):
        self.evidence["validation_status"] = "assessed"

        self.assertEqual(
            self.evidence["validation_status"],
            "assessed",
        )
        self.assertFalse(self.reassessment["triggered"])

    def test_02_reassessment_trigger_is_explicitly_represented(self):
        self.assertIn("triggered", self.reassessment)
        self.assertIn("reason", self.reassessment)

    def test_03_evidence_status_and_reassessment_trigger_are_distinct(self):
        self.evidence["validation_status"] = "rejected"

        self.assertEqual(
            self.evidence["validation_status"],
            "rejected",
        )
        self.assertFalse(self.reassessment["triggered"])

    def test_04_explicit_trigger_can_be_recorded_without_immediate_claim_status_change(self):
        self.reassessment["triggered"] = True
        self.reassessment["reason"] = "evidence-status-changed"

        self.assertTrue(self.reassessment["triggered"])
        self.assertEqual(
            self.claim["claim_status"],
            "recorded",
        )

    def test_05_trigger_references_the_same_claim_identity(self):
        self.reassessment["triggered"] = True

        self.assertEqual(
            self.reassessment["claim_id"],
            self.claim["claim_id"],
        )

    def test_06_trigger_state_does_not_replace_evidence_status(self):
        self.reassessment["triggered"] = True

        self.assertEqual(
            self.evidence["validation_status"],
            "unassessed",
        )
        self.assertTrue(self.reassessment["triggered"])


if __name__ == "__main__":
    unittest.main()
