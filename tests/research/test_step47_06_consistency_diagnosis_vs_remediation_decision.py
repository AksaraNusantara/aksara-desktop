import unittest


class TestConsistencyDiagnosisVsRemediationDecision(unittest.TestCase):
    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "claim_status": "approved",
        }

        self.transition_decision = {
            "decision_id": "decision-1",
            "claim_id": "claim-1",
            "target_status": "rejected",
        }

        self.consistency_diagnosis = {
            "diagnosis_id": "diagnosis-1",
            "claim_id": "claim-1",
            "source_decision_id": "decision-1",
            "status": "inconsistent",
        }

        self.remediation_decision = {
            "remediation_id": "remediation-1",
            "claim_id": "claim-1",
            "source_diagnosis_id": "diagnosis-1",
            "action": "manual_review",
        }

    def test_01_diagnosis_and_remediation_have_distinct_identities(self):
        self.assertNotEqual(
            self.consistency_diagnosis["diagnosis_id"],
            self.remediation_decision["remediation_id"],
        )

    def test_02_diagnosis_references_the_original_decision(self):
        self.assertEqual(
            self.consistency_diagnosis["source_decision_id"],
            self.transition_decision["decision_id"],
        )

    def test_03_remediation_references_the_diagnosis(self):
        self.assertEqual(
            self.remediation_decision["source_diagnosis_id"],
            self.consistency_diagnosis["diagnosis_id"],
        )

    def test_04_diagnosis_and_remediation_refer_to_the_same_claim(self):
        self.assertEqual(
            self.consistency_diagnosis["claim_id"],
            self.remediation_decision["claim_id"],
        )

    def test_05_diagnosis_value_is_not_the_remediation_action(self):
        self.assertNotEqual(
            self.consistency_diagnosis["status"],
            self.remediation_decision["action"],
        )

    def test_06_recording_remediation_decision_does_not_mutate_claim(self):
        original_status = self.claim["claim_status"]

        self.remediation_decision["action"] = "manual_review"

        self.assertEqual(
            self.claim["claim_status"],
            original_status,
        )


if __name__ == "__main__":
    unittest.main()