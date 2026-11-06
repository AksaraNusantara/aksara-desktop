import unittest


class TestStateMutationVsPostMutationStateVerification(unittest.TestCase):
    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "claim_status": "recorded",
        }

        self.mutation_record = {
            "mutation_id": "mutation-1",
            "claim_id": "claim-1",
            "previous_status": "recorded",
            "new_status": "rejected",
        }

    def test_01_actual_mutation_changes_claim_status(self):
        self.claim["claim_status"] = self.mutation_record["new_status"]

        self.assertEqual(
            self.claim["claim_status"],
            "rejected",
        )

    def test_02_actual_state_matches_mutation_record_after_mutation(self):
        self.claim["claim_status"] = self.mutation_record["new_status"]

        self.assertEqual(
            self.claim["claim_status"],
            self.mutation_record["new_status"],
        )

    def test_03_mutation_record_alone_does_not_change_claim_state(self):
        self.assertEqual(
            self.mutation_record["new_status"],
            "rejected",
        )

        self.assertEqual(
            self.claim["claim_status"],
            "recorded",
        )

    def test_04_state_verification_detects_unapplied_mutation(self):
        expected_status = self.mutation_record["new_status"]
        actual_status = self.claim["claim_status"]

        self.assertNotEqual(
            actual_status,
            expected_status,
        )

    def test_05_state_verification_confirms_applied_mutation(self):
        self.claim["claim_status"] = self.mutation_record["new_status"]

        actual_status = self.claim["claim_status"]
        expected_status = self.mutation_record["new_status"]

        self.assertEqual(
            actual_status,
            expected_status,
        )

    def test_06_mutation_preserves_previous_status_in_record(self):
        previous_status = self.claim["claim_status"]

        self.claim["claim_status"] = self.mutation_record["new_status"]

        self.assertEqual(
            self.mutation_record["previous_status"],
            previous_status,
        )

        self.assertEqual(
            self.claim["claim_status"],
            "rejected",
        )


if __name__ == "__main__":
    unittest.main()