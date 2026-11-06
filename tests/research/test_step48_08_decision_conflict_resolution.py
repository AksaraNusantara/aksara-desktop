import unittest


class TestStep48DecisionConflictResolution(unittest.TestCase):

    def setUp(self):
        self.model = {
            "result": {
                "result_id": "result-1",
                "value": "invalid",
            },
            "decisions": [
                {
                    "decision_id": "decision-1",
                    "value": "reject",
                },
                {
                    "decision_id": "decision-2",
                    "value": "request-revision",
                },
            ],
            "resolution": None,
            "mutation": None,
            "state": "draft",
        }

    def test_01_multiple_decisions_can_coexist(self):
        self.assertEqual(
            len(self.model["decisions"]),
            2,
        )

    def test_02_conflicting_decisions_can_be_detected(self):
        decisions = {
            decision["value"]
            for decision in self.model["decisions"]
        }

        self.assertEqual(
            decisions,
            {
                "reject",
                "request-revision",
            },
        )

    def test_03_conflict_does_not_automatically_mutate_state(self):
        original_state = self.model["state"]

        self.assertIsNone(
            self.model["resolution"],
        )

        self.assertIsNone(
            self.model["mutation"],
        )

        self.assertEqual(
            self.model["state"],
            original_state,
        )

    def test_04_resolution_can_be_recorded_separately(self):
        self.model["resolution"] = {
            "resolution_id": "resolution-1",
            "selected_decision_id": "decision-2",
        }

        self.assertIsNotNone(
            self.model["resolution"],
        )

        self.assertIsNone(
            self.model["mutation"],
        )

    def test_05_resolution_does_not_automatically_mutate_state(self):
        original_state = self.model["state"]

        self.model["resolution"] = {
            "resolution_id": "resolution-1",
            "selected_decision_id": "decision-2",
        }

        self.assertEqual(
            self.model["state"],
            original_state,
        )

        self.assertIsNone(
            self.model["mutation"],
        )

    def test_06_mutation_can_reference_resolution_explicitly(self):
        self.model["resolution"] = {
            "resolution_id": "resolution-1",
            "selected_decision_id": "decision-2",
        }

        self.model["mutation"] = {
            "mutation_id": "mutation-1",
            "source_resolution_id": "resolution-1",
            "target_state": "revision-required",
        }

        self.assertEqual(
            self.model["mutation"]["source_resolution_id"],
            self.model["resolution"]["resolution_id"],
        )

        self.assertEqual(
            self.model["state"],
            "draft",
        )


if __name__ == "__main__":
    unittest.main()