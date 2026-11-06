import unittest


class TestStep48MultipleInterpretationsDecisions(unittest.TestCase):

    def setUp(self):
        self.validation = {
            "result_id": "result-1",
            "result": "invalid",
            "interpretations": [
                {
                    "interpretation_id": "interpretation-1",
                    "value": "schema-mismatch",
                    "decision": None,
                },
                {
                    "interpretation_id": "interpretation-2",
                    "value": "missing-required-field",
                    "decision": None,
                },
            ],
        }

    def test_01_multiple_interpretations_reference_same_result(self):
        self.assertEqual(
            len(self.validation["interpretations"]),
            2,
        )

        self.assertEqual(
            self.validation["result_id"],
            "result-1",
        )

    def test_02_first_interpretation_can_have_decision(self):
        self.validation["interpretations"][0]["decision"] = "reject"

        self.assertEqual(
            self.validation["interpretations"][0]["decision"],
            "reject",
        )

        self.assertIsNone(
            self.validation["interpretations"][1]["decision"],
        )

    def test_03_second_interpretation_can_have_different_decision(self):
        self.validation["interpretations"][1]["decision"] = (
            "request-revision"
        )

        self.assertEqual(
            self.validation["interpretations"][1]["decision"],
            "request-revision",
        )

        self.assertIsNone(
            self.validation["interpretations"][0]["decision"],
        )

    def test_04_decision_does_not_change_interpretation_value(self):
        original_value = (
            self.validation["interpretations"][0]["value"]
        )

        self.validation["interpretations"][0]["decision"] = "reject"

        self.assertEqual(
            self.validation["interpretations"][0]["value"],
            original_value,
        )

    def test_05_decision_does_not_change_result(self):
        original_result = self.validation["result"]

        self.validation["interpretations"][0]["decision"] = "reject"
        self.validation["interpretations"][1]["decision"] = (
            "request-revision"
        )

        self.assertEqual(
            self.validation["result"],
            original_result,
        )

    def test_06_multiple_interpretive_paths_can_coexist(self):
        self.validation["interpretations"][0]["decision"] = "reject"
        self.validation["interpretations"][1]["decision"] = (
            "request-revision"
        )

        decisions = [
            item["decision"]
            for item in self.validation["interpretations"]
        ]

        self.assertEqual(
            decisions,
            [
                "reject",
                "request-revision",
            ],
        )


if __name__ == "__main__":
    unittest.main()