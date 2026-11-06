import unittest


class TestStep48ResultMultipleInterpretations(unittest.TestCase):

    def setUp(self):
        self.validation = {
            "result_id": "result-1",
            "result": "invalid",
            "interpretations": [],
        }

    def test_01_single_result_can_have_multiple_interpretations(self):
        self.validation["interpretations"].append(
            "missing-required-field"
        )

        self.validation["interpretations"].append(
            "schema-mismatch"
        )

        self.validation["interpretations"].append(
            "manual-review-required"
        )

        self.assertEqual(
            len(self.validation["interpretations"]),
            3,
        )

    def test_02_result_identity_remains_stable(self):
        original_id = self.validation["result_id"]

        self.validation["interpretations"].append(
            "missing-required-field"
        )

        self.validation["interpretations"].append(
            "schema-mismatch"
        )

        self.assertEqual(
            self.validation["result_id"],
            original_id,
        )

    def test_03_result_value_remains_stable(self):
        original_result = self.validation["result"]

        self.validation["interpretations"].append(
            "missing-required-field"
        )

        self.validation["interpretations"].append(
            "schema-mismatch"
        )

        self.assertEqual(
            self.validation["result"],
            original_result,
        )

    def test_04_interpretations_are_distinct_values(self):
        self.validation["interpretations"] = [
            "missing-required-field",
            "schema-mismatch",
            "manual-review-required",
        ]

        self.assertEqual(
            len(set(self.validation["interpretations"])),
            3,
        )

    def test_05_adding_interpretation_does_not_mutate_result(self):
        original_result = self.validation["result"]

        self.validation["interpretations"].append(
            "missing-required-field"
        )

        self.assertEqual(
            self.validation["result"],
            original_result,
        )

    def test_06_multiple_interpretations_can_coexist(self):
        self.validation["interpretations"] = [
            "missing-required-field",
            "schema-mismatch",
        ]

        self.assertIn(
            "missing-required-field",
            self.validation["interpretations"],
        )

        self.assertIn(
            "schema-mismatch",
            self.validation["interpretations"],
        )


if __name__ == "__main__":
    unittest.main()