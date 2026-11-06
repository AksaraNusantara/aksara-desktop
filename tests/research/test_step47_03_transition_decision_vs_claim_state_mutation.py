import unittest


class TestTransitionDecisionVsClaimStateMutation(unittest.TestCase):
    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "claim_status": "recorded",
        }

        self.transition_decision = {
            "decision_id": "decision-1",
            "claim_id": "claim-1",
            "decision": "status-change-approved",
            "target_status": "rejected",
        }

        self.state_mutation = {
            "mutation_id": "mutation-1",
            "claim_id": "claim-1",
            "source_decision_id": "decision-1",
            "previous_status": "recorded",
            "new_status": "rejected",
        }

    def test_01_decision_and_mutation_have_distinct_identities(self):
        self.assertNotEqual(
            self.transition_decision["decision_id"],
            self.state_mutation["mutation_id"],
        )

    def test_02_mutation_references_the_transition_decision(self):
        self.assertEqual(
            self.state_mutation["source_decision_id"],
            self.transition_decision["decision_id"],
        )

    def test_03_decision_and_mutation_refer_to_the_same_claim(self):
        self.assertEqual(
            self.transition_decision["claim_id"],
            self.state_mutation["claim_id"],
        )

    def test_04_decision_target_matches_mutation_target(self):
        self.assertEqual(
            self.transition_decision["target_status"],
            self.state_mutation["new_status"],
        )

    def test_05_mutation_records_previous_and_new_status(self):
        self.assertEqual(
            self.state_mutation["previous_status"],
            "recorded",
        )
        self.assertEqual(
            self.state_mutation["new_status"],
            "rejected",
        )

    def test_06_recorded_decision_and_mutation_do_not_mutate_claim_automatically(self):
        self.assertEqual(
            self.claim["claim_status"],
            "recorded",
        )

        self.assertEqual(
            self.transition_decision["decision"],
            "status-change-approved",
        )

        self.assertEqual(
            self.state_mutation["new_status"],
            "rejected",
        )

        # The fixture records a decision and a mutation description,
        # but does not implement the operation that changes Claim State.
        self.assertEqual(
            self.claim["claim_status"],
            "recorded",
        )


if __name__ == "__main__":
    unittest.main()