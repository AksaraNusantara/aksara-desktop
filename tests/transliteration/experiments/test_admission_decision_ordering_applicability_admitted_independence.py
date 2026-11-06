import unittest


def evaluate_applicability(scope, resolution):
    return resolution["allowed_scope"] == scope


def evaluate_admission(applicable, admission_policy):
    if not applicable:
        return "REJECTED"

    return admission_policy


class TestAdmissionDecisionOrderingApplicabilityAdmittedIndependence(
    unittest.TestCase
):

    def test_applicable_request_can_be_accepted(self):
        applicable = evaluate_applicability(
            "scope-a",
            {
                "allowed_scope": "scope-a",
            },
        )

        admission = evaluate_admission(
            applicable,
            "ACCEPTED",
        )

        self.assertTrue(applicable)
        self.assertEqual(admission, "ACCEPTED")

    def test_applicable_request_can_be_rejected_by_other_admission_input(
        self,
    ):
        applicable = evaluate_applicability(
            "scope-a",
            {
                "allowed_scope": "scope-a",
            },
        )

        admission = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertTrue(applicable)
        self.assertEqual(admission, "REJECTED")

    def test_applicability_does_not_force_acceptance(self):
        applicable = True

        admission = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertTrue(applicable)
        self.assertEqual(admission, "REJECTED")

    def test_applicability_can_be_true_before_admission(self):
        applicable = evaluate_applicability(
            "scope-a",
            {
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(applicable)

    def test_admission_can_depend_on_policy_beyond_applicability(
        self,
    ):
        applicable = True

        admission_a = evaluate_admission(
            applicable,
            "ACCEPTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertNotEqual(
            admission_a,
            admission_b,
        )

    def test_same_applicability_can_produce_different_admission_results(
        self,
    ):
        applicable = True

        results = [
            evaluate_admission(
                applicable,
                "ACCEPTED",
            ),
            evaluate_admission(
                applicable,
                "REJECTED",
            ),
        ]

        self.assertEqual(
            results,
            ["ACCEPTED", "REJECTED"],
        )

    def test_resolution_can_remain_unchanged_while_admission_changes(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        applicable = evaluate_applicability(
            "scope-a",
            resolution,
        )

        admission_a = evaluate_admission(
            applicable,
            "ACCEPTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertTrue(applicable)
        self.assertEqual(
            admission_a,
            "ACCEPTED",
        )
        self.assertEqual(
            admission_b,
            "REJECTED",
        )

        self.assertEqual(
            resolution["allowed_scope"],
            "scope-a",
        )

    def test_scope_can_remain_unchanged_while_admission_changes(
        self,
    ):
        scope = "scope-a"

        applicable = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        admission_a = evaluate_admission(
            applicable,
            "ACCEPTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertTrue(applicable)
        self.assertNotEqual(
            admission_a,
            admission_b,
        )

    def test_admission_decision_is_not_applicability_value(
        self,
    ):
        applicable = True

        admission = evaluate_admission(
            applicable,
            "ACCEPTED",
        )

        self.assertNotEqual(
            applicable,
            admission,
        )

    def test_applicability_and_admission_can_be_observed_separately(
        self,
    ):
        applicable = True

        observation = {
            "applicable": applicable,
            "admission": "REJECTED",
        }

        self.assertTrue(
            observation["applicable"]
        )

        self.assertEqual(
            observation["admission"],
            "REJECTED",
        )

    def test_applicable_resolution_can_be_rejected_without_mutating_resolution(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        applicable = evaluate_applicability(
            "scope-a",
            resolution,
        )

        admission = evaluate_admission(
            applicable,
            "REJECTED",
        )

        self.assertTrue(applicable)
        self.assertEqual(
            admission,
            "REJECTED",
        )

        self.assertEqual(
            resolution["allowed_scope"],
            "scope-a",
        )

    def test_acceptance_is_an_admission_semantic_not_an_applicability_semantic(
        self,
    ):
        applicable = True
        admission = "ACCEPTED"

        self.assertTrue(applicable)
        self.assertEqual(admission, "ACCEPTED")

        self.assertNotEqual(
            type(applicable),
            type(admission),
        )

    def test_minimal_model_preserves_independence(self):
        applicable = True
        admission = "REJECTED"

        relationship = {
            "applicable": applicable,
            "admission": admission,
        }

        self.assertTrue(
            relationship["applicable"]
        )

        self.assertEqual(
            relationship["admission"],
            "REJECTED",
        )


if __name__ == "__main__":
    unittest.main()