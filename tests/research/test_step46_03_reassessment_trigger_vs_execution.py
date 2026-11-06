
import unittest


class TestReassessmentTriggerVsExecution(unittest.TestCase):

    def setUp(self):
        self.reassessment = {
            "reassessment_id": "reassessment-1",
            "claim_id": "claim-1",
            "triggered": True,
            "execution_status": "not_started",
            "result": None,
        }

    def test_01_trigger_can_exist_before_execution(self):
        self.assertTrue(self.reassessment["triggered"])
        self.assertEqual(
            self.reassessment["execution_status"],
            "not_started",
        )

    def test_02_trigger_and_execution_status_are_separate_fields(self):
        self.assertIn("triggered", self.reassessment)
        self.assertIn("execution_status", self.reassessment)

    def test_03_not_started_execution_has_no_result(self):
        self.assertEqual(
            self.reassessment["execution_status"],
            "not_started",
        )
        self.assertIsNone(self.reassessment["result"])

    def test_04_execution_can_be_marked_started_without_result(self):
        self.reassessment["execution_status"] = "running"

        self.assertEqual(
            self.reassessment["execution_status"],
            "running",
        )
        self.assertIsNone(self.reassessment["result"])

    def test_05_execution_result_is_distinct_from_trigger(self):
        self.reassessment["execution_status"] = "completed"
        self.reassessment["result"] = "claim-retained"

        self.assertTrue(self.reassessment["triggered"])
        self.assertEqual(
            self.reassessment["execution_status"],
            "completed",
        )
        self.assertEqual(
            self.reassessment["result"],
            "claim-retained",
        )

    def test_06_execution_state_changes_preserve_reassessment_identity(self):
        reassessment_id = self.reassessment["reassessment_id"]

        self.reassessment["execution_status"] = "running"
        self.reassessment["execution_status"] = "completed"
        self.reassessment["result"] = "claim-retained"

        self.assertEqual(
            self.reassessment["reassessment_id"],
            reassessment_id,
        )


if __name__ == "__main__":
    unittest.main()
