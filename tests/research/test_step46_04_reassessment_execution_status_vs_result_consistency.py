
import unittest


class TestReassessmentExecutionStatusVsResultConsistency(unittest.TestCase):

    def setUp(self):
        self.reassessment = {
            "reassessment_id": "reassessment-1",
            "execution_status": "completed",
            "result": None,
        }

    def test_01_execution_status_is_explicitly_recorded(self):
        self.assertEqual(
            self.reassessment["execution_status"],
            "completed",
        )

    def test_02_result_is_a_separate_attribute(self):
        self.assertIn("result", self.reassessment)
        self.assertIsNone(self.reassessment["result"])

    def test_03_completed_status_can_coexist_with_missing_result_in_the_fixture(self):
        self.assertEqual(
            self.reassessment["execution_status"],
            "completed",
        )
        self.assertIsNone(self.reassessment["result"])

    def test_04_adding_result_does_not_change_execution_identity(self):
        reassessment_id = self.reassessment["reassessment_id"]

        self.reassessment["result"] = "claim-retained"

        self.assertEqual(
            self.reassessment["reassessment_id"],
            reassessment_id,
        )

    def test_05_result_can_be_recorded_without_replacing_execution_status(self):
        self.reassessment["result"] = "claim-retained"

        self.assertEqual(
            self.reassessment["execution_status"],
            "completed",
        )
        self.assertEqual(
            self.reassessment["result"],
            "claim-retained",
        )

    def test_06_status_and_result_require_a_contract_for_consistency_validation(self):
        self.assertIn("execution_status", self.reassessment)
        self.assertIn("result", self.reassessment)

        # This fixture defines no rule that declares this combination
        # valid or invalid. It only confirms both attributes exist.
        self.assertEqual(
            self.reassessment["execution_status"],
            "completed",
        )
        self.assertIsNone(self.reassessment["result"])


if __name__ == "__main__":
    unittest.main()
