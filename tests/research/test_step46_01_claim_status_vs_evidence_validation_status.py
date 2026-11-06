
import unittest


class TestClaimStatusVsEvidenceValidationStatus(unittest.TestCase):

    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "event_id": "event-B",
            "causes": ["event-A"],
            "claim_status": "recorded",
        }

        self.evidence = {
            "evidence_id": "evidence-1",
            "claim_id": "claim-1",
            "validation_status": "unassessed",
        }

    def test_01_claim_and_evidence_have_distinct_identities(self):
        self.assertNotEqual(
            self.claim["claim_id"],
            self.evidence["evidence_id"],
        )

    def test_02_claim_status_and_evidence_status_are_separate_fields(self):
        self.assertIn("claim_status", self.claim)
        self.assertIn("validation_status", self.evidence)

    def test_03_evidence_references_the_claim_without_becoming_the_claim(self):
        self.assertEqual(
            self.evidence["claim_id"],
            self.claim["claim_id"],
        )
        self.assertNotEqual(
            self.evidence["evidence_id"],
            self.claim["claim_id"],
        )

    def test_04_evidence_status_can_change_while_claim_status_remains_unchanged(self):
        original_claim_status = self.claim["claim_status"]

        self.evidence["validation_status"] = "assessed"

        self.assertEqual(
            self.claim["claim_status"],
            original_claim_status,
        )
        self.assertEqual(
            self.evidence["validation_status"],
            "assessed",
        )

    def test_05_claim_status_can_change_without_changing_evidence_status(self):
        original_evidence_status = self.evidence["validation_status"]

        self.claim["claim_status"] = "under_review"

        self.assertEqual(
            self.claim["claim_status"],
            "under_review",
        )
        self.assertEqual(
            self.evidence["validation_status"],
            original_evidence_status,
        )

    def test_06_status_changes_do_not_change_claim_or_evidence_identity(self):
        claim_id_before = self.claim["claim_id"]
        evidence_id_before = self.evidence["evidence_id"]

        self.claim["claim_status"] = "under_review"
        self.evidence["validation_status"] = "assessed"

        self.assertEqual(self.claim["claim_id"], claim_id_before)
        self.assertEqual(
            self.evidence["evidence_id"],
            evidence_id_before,
        )


if __name__ == "__main__":
    unittest.main()
