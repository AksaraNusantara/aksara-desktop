import unittest


class TestStep48InterpretationDecisionGeneralization(unittest.TestCase):

    def setUp(self):
        self.transliteration = {
            "result": "hanacaraka",
            "interpretation": "conversion-successful",
            "decision": None,
        }

        self.claim_assessment = {
            "result": "claim-rejected",
            "interpretation": "claim-not-supported",
            "decision": None,
        }

        self.document_validation = {
            "result": "invalid",
            "interpretation": "validation-failed",
            "decision": None,
        }

    # ---------------------------------------------------------
    # 48-3-A — Interpretation can exist without Decision
    # ---------------------------------------------------------

    def test_01_transliteration_interpretation_can_exist_without_decision(self):
        self.assertIsNotNone(
            self.transliteration["interpretation"],
        )

        self.assertIsNone(
            self.transliteration["decision"],
        )

    def test_02_claim_interpretation_can_exist_without_decision(self):
        self.assertIsNotNone(
            self.claim_assessment["interpretation"],
        )

        self.assertIsNone(
            self.claim_assessment["decision"],
        )

    def test_03_document_interpretation_can_exist_without_decision(self):
        self.assertIsNotNone(
            self.document_validation["interpretation"],
        )

        self.assertIsNone(
            self.document_validation["decision"],
        )

    # ---------------------------------------------------------
    # 48-3-B — Decision is not automatically mutated
    # ---------------------------------------------------------

    def test_04_changing_transliteration_interpretation_does_not_create_decision(self):
        original_decision = self.transliteration["decision"]

        self.transliteration["interpretation"] = "conversion-needs-review"

        self.assertEqual(
            self.transliteration["decision"],
            original_decision,
        )

    def test_05_changing_claim_interpretation_does_not_create_decision(self):
        original_decision = self.claim_assessment["decision"]

        self.claim_assessment["interpretation"] = "claim-requires-review"

        self.assertEqual(
            self.claim_assessment["decision"],
            original_decision,
        )

    def test_06_changing_document_interpretation_does_not_create_decision(self):
        original_decision = self.document_validation["decision"]

        self.document_validation["interpretation"] = "validation-requires-review"

        self.assertEqual(
            self.document_validation["decision"],
            original_decision,
        )


if __name__ == "__main__":
    unittest.main()