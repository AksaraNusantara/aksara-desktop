import unittest


def evaluate_applicability(scope, resolution):
    return resolution["allowed_scope"] == scope


def evaluate_admission(applicable, capacity_available, policy):
    if policy == "require_applicability" and not applicable:
        return "REJECTED"

    if not capacity_available:
        return "REJECTED"

    return "ACCEPTED"


class TestAdmissionDecisionOrderingApplicabilityVsAdmissionInputs(
    unittest.TestCase
):

    def test_applicability_can_be_one_admission_input(self):
        admission = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="require_applicability",
        )

        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_other_input_can_change_admission_while_applicability_stays_true(
        self,
    ):
        applicable = True

        accepted = evaluate_admission(
            applicable,
            capacity_available=True,
            policy="require_applicability",
        )

        rejected = evaluate_admission(
            applicable,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertTrue(applicable)
        self.assertEqual(accepted, "ACCEPTED")
        self.assertEqual(rejected, "REJECTED")

    def test_admission_is_not_determined_by_applicability_alone(
        self,
    ):
        applicable = True

        admission = evaluate_admission(
            applicable,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertTrue(applicable)
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_applicability_can_change_while_other_input_stays_constant(
        self,
    ):
        capacity_available = True

        accepted = evaluate_admission(
            applicable=True,
            capacity_available=capacity_available,
            policy="require_applicability",
        )

        rejected = evaluate_admission(
            applicable=False,
            capacity_available=capacity_available,
            policy="require_applicability",
        )

        self.assertEqual(accepted, "ACCEPTED")
        self.assertEqual(rejected, "REJECTED")

    def test_policy_can_determine_whether_applicability_matters(
        self,
    ):
        applicable = False
        capacity_available = True

        required = evaluate_admission(
            applicable,
            capacity_available,
            policy="require_applicability",
        )

        permissive = evaluate_admission(
            applicable,
            capacity_available,
            policy="ignore_applicability",
        )

        self.assertEqual(required, "REJECTED")
        self.assertEqual(permissive, "ACCEPTED")

    def test_same_applicability_and_capacity_can_produce_different_results_under_policy(
        self,
    ):
        applicable = False
        capacity_available = True

        result_a = evaluate_admission(
            applicable,
            capacity_available,
            policy="require_applicability",
        )

        result_b = evaluate_admission(
            applicable,
            capacity_available,
            policy="ignore_applicability",
        )

        self.assertEqual(result_a, "REJECTED")
        self.assertEqual(result_b, "ACCEPTED")

    def test_applicability_evaluation_is_separate_from_admission_evaluation(
        self,
    ):
        applicability = evaluate_applicability(
            "scope-a",
            {
                "allowed_scope": "scope-a",
            },
        )

        admission = evaluate_admission(
            applicability,
            capacity_available=True,
            policy="require_applicability",
        )

        self.assertTrue(applicability)
        self.assertEqual(admission, "ACCEPTED")

    def test_resolution_can_remain_unchanged_while_admission_changes(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        applicability = evaluate_applicability(
            "scope-a",
            resolution,
        )

        admission_a = evaluate_admission(
            applicability,
            capacity_available=True,
            policy="require_applicability",
        )

        admission_b = evaluate_admission(
            applicability,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertTrue(applicability)
        self.assertEqual(admission_a, "ACCEPTED")
        self.assertEqual(admission_b, "REJECTED")
        self.assertEqual(
            resolution["allowed_scope"],
            "scope-a",
        )

    def test_scope_can_remain_unchanged_while_admission_changes(
        self,
    ):
        scope = "scope-a"

        applicability = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        admission_a = evaluate_admission(
            applicability,
            capacity_available=True,
            policy="require_applicability",
        )

        admission_b = evaluate_admission(
            applicability,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertTrue(applicability)
        self.assertNotEqual(
            admission_a,
            admission_b,
        )

    def test_admission_inputs_can_be_observed_without_mutating_applicability(
        self,
    ):
        applicability = True

        before = applicability

        evaluate_admission(
            applicability,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertEqual(
            applicability,
            before,
        )

    def test_applicability_does_not_require_admission_identity(
        self,
    ):
        applicability = True

        result = {
            "applicable": applicability,
        }

        self.assertNotIn(
            "admission_id",
            result,
        )

    def test_admission_does_not_require_applicability_identity(
        self,
    ):
        admission = "ACCEPTED"

        result = {
            "admission": admission,
        }

        self.assertNotIn(
            "applicability_id",
            result,
        )

    def test_minimal_model_preserves_multiple_admission_inputs(
        self,
    ):
        relationship = {
            "applicable": True,
            "capacity_available": False,
            "policy": "require_applicability",
        }

        admission = evaluate_admission(
            relationship["applicable"],
            relationship["capacity_available"],
            relationship["policy"],
        )

        self.assertTrue(
            relationship["applicable"]
        )

        self.assertFalse(
            relationship["capacity_available"]
        )

        self.assertEqual(
            admission,
            "REJECTED",
        )


if __name__ == "__main__":
    unittest.main()