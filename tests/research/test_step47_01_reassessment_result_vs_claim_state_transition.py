import unittest


class TestReassessmentResultVsClaimStateTransition(unittest.TestCase):
    def setUp(self):
        self.claim = {
            "claim_id": "claim-1",
            "claim_status": "recorded",
        }

        self.reassessment = {
            "reassessment_id": "reassessment-1",
            "claim_id": "claim-1",
            "execution_status": "completed",
            "result": "claim-retained",
        }

    def test_01_claim_and_reassessment_have_distinct_identities(self):
        self.assertNotEqual(
            self.claim["claim_id"],
            self.reassessment["reassessment_id"],
        )

    def test_02_reassessment_references_the_claim(self):
        self.assertEqual(
            self.reassessment["claim_id"],
            self.claim["claim_id"],
        )

    def test_03_reassessment_result_is_explicitly_recorded(self):
        self.assertEqual(
            self.reassessment["result"],
            "claim-retained",
        )

    def test_04_result_can_coexist_with_unchanged_claim_status_in_fixture(self):
        self.assertEqual(
            self.reassessment["result"],
            "claim-retained",
        )
        self.assertEqual(
            self.claim["claim_status"],
            "recorded",
        )

    def test_05_claim_status_and_reassessment_result_are_separate_fields(self):
        self.assertIn("claim_status", self.claim)
        self.assertIn("result", self.reassessment)

    def test_06_recording_result_does_not_change_claim_identity(self):
        claim_id_before = self.claim["claim_id"]

        self.reassessment["result"] = "claim-retained"

        self.assertEqual(
            self.claim["claim_id"],
            claim_id_before,
        )


if __name__ == "__main__":
    unittest.main()