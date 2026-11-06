import unittest


class TestTransitionIntentVsAppliedStateConsistency(unittest.TestCase):
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

    def test_01_decision_and_claim_have_distinct_identities(self):
        self.assertNotEqual(
            self.transition_decision["decision_id"],
            self.claim["claim_id"],
        )

    def test_02_decision_references_the_claim(self):
        self.assertEqual(
            self.transition_decision["claim_id"],
            self.claim["claim_id"],
        )

    def test_03_target_status_can_be_compared_with_actual_state(self):
        self.assertNotEqual(
            self.transition_decision["target_status"],
            self.claim["claim_status"],
        )

    def test_04_inconsistency_can_be_detected_without_mutating_claim(self):
        expected_status = self.transition_decision["target_status"]
        actual_status = self.claim["claim_status"]

        self.assertNotEqual(
            expected_status,
            actual_status,
        )

        self.assertEqual(
            self.claim["claim_status"],
            "approved",
        )

    def test_05_consistency_diagnosis_does_not_change_decision_identity(self):
        decision_id_before = self.transition_decision["decision_id"]

        is_consistent = (
            self.transition_decision["target_status"]
            == self.claim["claim_status"]
        )

        self.assertFalse(is_consistent)

        self.assertEqual(
            self.transition_decision["decision_id"],
            decision_id_before,
        )

    def test_06_consistency_diagnosis_does_not_change_claim_identity(self):
        claim_id_before = self.claim["claim_id"]

        is_consistent = (
            self.transition_decision["target_status"]
            == self.claim["claim_status"]
        )

        self.assertFalse(is_consistent)

        self.assertEqual(
            self.claim["claim_id"],
            claim_id_before,
        )


if __name__ == "__main__":
    unittest.main()