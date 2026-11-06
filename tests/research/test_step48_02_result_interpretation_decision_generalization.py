import unittest


class TestStep48ResultInterpretationDecisionGeneralization(unittest.TestCase):

    def setUp(self):
        self.transliteration = {
            "result": "hanacaraka",
            "interpretation": None,
            "decision": None,
        }

        self.claim_assessment = {
            "result": "claim-rejected",
            "interpretation": None,
            "decision": None,
        }

        self.document_validation = {
            "result": "invalid",
            "interpretation": None,
            "decision": None,
        }

    # ---------------------------------------------------------
    # 48-2-A — Transliteration
    # ---------------------------------------------------------

    def test_01_transliteration_result_can_be_interpreted_before_decision(self):
        self.transliteration["interpretation"] = "conversion-successful"

        self.assertEqual(
            self.transliteration["result"],
            "hanacaraka",
        )

        self.assertEqual(
            self.transliteration["interpretation"],
            "conversion-successful",
        )

        self.assertIsNone(
            self.transliteration["decision"],
        )

    # ---------------------------------------------------------
    # 48-2-B — Claim Assessment
    # ---------------------------------------------------------

    def test_02_claim_result_can_be_interpreted_before_decision(self):
        self.claim_assessment["interpretation"] = "claim-not-supported"

        self.assertEqual(
            self.claim_assessment["result"],
            "claim-rejected",
        )

        self.assertEqual(
            self.claim_assessment["interpretation"],
            "claim-not-supported",
        )

        self.assertIsNone(
            self.claim_assessment["decision"],
        )

    # ---------------------------------------------------------
    # 48-2-C — Document Validation
    # ---------------------------------------------------------

    def test_03_document_result_can_be_interpreted_before_decision(self):
        self.document_validation["interpretation"] = "validation-failed"

        self.assertEqual(
            self.document_validation["result"],
            "invalid",
        )

        self.assertEqual(
            self.document_validation["interpretation"],
            "validation-failed",
        )

        self.assertIsNone(
            self.document_validation["decision"],
        )

    # ---------------------------------------------------------
    # 48-2-D — Interpretation does not mutate Result
    # ---------------------------------------------------------

    def test_04_interpretation_does_not_mutate_transliteration_result(self):
        original_result = self.transliteration["result"]

        self.transliteration["interpretation"] = "conversion-successful"

        self.assertEqual(
            self.transliteration["result"],
            original_result,
        )

    def test_05_interpretation_does_not_mutate_claim_result(self):
        original_result = self.claim_assessment["result"]

        self.claim_assessment["interpretation"] = "claim-not-supported"

        self.assertEqual(
            self.claim_assessment["result"],
            original_result,
        )

    def test_06_interpretation_does_not_mutate_document_result(self):
        original_result = self.document_validation["result"]

        self.document_validation["interpretation"] = "validation-failed"

        self.assertEqual(
            self.document_validation["result"],
            original_result,
        )


if __name__ == "__main__":
    unittest.main()