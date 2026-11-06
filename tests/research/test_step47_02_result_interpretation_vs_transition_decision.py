import unittest


class TestResultInterpretationVsTransitionDecision(unittest.TestCase):
    def setUp(self):
        self.reassessment = {
            "reassessment_id": "reassessment-1",
            "claim_id": "claim-1",
            "execution_status": "completed",
            "result": "claim-rejected",
        }

        self.transition_decision = {
            "decision_id": "decision-1",
            "claim_id": "claim-1",
            "source_reassessment_id": "reassessment-1",
            "decision": "status-change-approved",
        }

    def test_01_result_and_transition_decision_have_distinct_fields(self):
        self.assertIn("result", self.reassessment)
        self.assertIn("decision", self.transition_decision)

    def test_02_result_and_transition_decision_have_distinct_identities(self):
        self.assertNotEqual(
            self.reassessment["reassessment_id"],
            self.transition_decision["decision_id"],
        )

    def test_03_transition_decision_references_the_reassessment(self):
        self.assertEqual(
            self.transition_decision["source_reassessment_id"],
            self.reassessment["reassessment_id"],
        )

    def test_04_result_value_does_not_equal_transition_decision_value(self):
        self.assertNotEqual(
            self.reassessment["result"],
            self.transition_decision["decision"],
        )

    def test_05_result_and_decision_refer_to_the_same_claim(self):
        self.assertEqual(
            self.reassessment["claim_id"],
            self.transition_decision["claim_id"],
        )

    def test_06_transition_decision_can_be_recorded_without_mutating_result(self):
        original_result = self.reassessment["result"]

        self.transition_decision["decision"] = "status-change-approved"

        self.assertEqual(
            self.reassessment["result"],
            original_result,
        )


if __name__ == "__main__":
    unittest.main()