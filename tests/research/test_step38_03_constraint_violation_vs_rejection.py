import unittest


def make_constraint(name, rule):
    return {
        "name": name,
        "rule": rule,
    }


def evaluate_constraint(constraint, result):
    return {
        "constraint": constraint,
        "result": result,
    }


def evaluate_admission(inputs):
    return inputs["admission_result"]


class TestConstraintViolationVsRejection(unittest.TestCase):

    def test_01_violation_is_distinct_from_rejection(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        rejection = "REJECTED"

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertNotEqual(
            evaluation["result"],
            rejection,
        )

    def test_02_violation_can_exist_without_admission_decision(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertNotIn(
            "admission",
            evaluation,
        )

    def test_03_violation_can_be_input_to_admission_evaluation(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "REJECTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_04_admission_result_is_distinct_from_constraint_result(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            admission,
            "ACCEPTED",
        )
        self.assertNotEqual(
            evaluation["result"],
            admission,
        )

    def test_05_same_violation_can_participate_in_different_admission_results(self):
        constraint = make_constraint(
            "request_required",
            "request_must_exist",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        result_a = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "REJECTED",
            }
        )

        result_b = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertNotEqual(
            result_a,
            result_b,
        )

    def test_06_violation_does_not_determine_admission_intrinsically(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        result_a = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "REJECTED",
            }
        )

        result_b = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "ACCEPTED",
            }
        )

        self.assertNotEqual(
            result_a,
            result_b,
        )

    def test_07_policy_can_mediate_violation_and_admission(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        strict_result = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "policy": "STRICT",
                "admission_result": "REJECTED",
            }
        )

        lenient_result = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "policy": "LENIENT",
                "admission_result": "ACCEPTED",
            }
        )

        self.assertNotEqual(
            strict_result,
            lenient_result,
        )

    def test_08_policy_is_distinct_from_violation(self):
        evaluation = {
            "result": "VIOLATED",
        }

        policy = "STRICT"

        self.assertNotEqual(
            evaluation["result"],
            policy,
        )

    def test_09_policy_is_distinct_from_admission(self):
        policy = "STRICT"
        admission = "REJECTED"

        self.assertNotEqual(
            policy,
            admission,
        )

    def test_10_violation_does_not_mutate_constraint(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        original = dict(constraint)

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            constraint,
            original,
        )

    def test_11_admission_evaluation_does_not_mutate_constraint(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        original = dict(constraint)

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "REJECTED",
            }
        )

        self.assertEqual(
            constraint,
            original,
        )

    def test_12_violation_does_not_change_constraint_identity(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        constraint_id = "C1"

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            constraint_id,
            "C1",
        )

    def test_13_violation_does_not_create_admission_identity(self):
        evaluation = {
            "result": "VIOLATED",
        }

        admission_id = None

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertIsNone(admission_id)

    def test_14_violation_and_admission_can_be_observed_separately(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        constraint_observation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission_observation = {
            "decision": "REJECTED",
        }

        self.assertEqual(
            constraint_observation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            admission_observation["decision"],
            "REJECTED",
        )

    def test_15_violation_is_not_admission_state(self):
        evaluation = {
            "result": "VIOLATED",
        }

        admission_states = {
            "ACCEPTED",
            "REJECTED",
        }

        self.assertNotIn(
            evaluation["result"],
            admission_states,
        )

    def test_16_rejection_is_not_constraint_result(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        evaluation = evaluate_constraint(
            constraint,
            "SATISFIED",
        )

        admission = "REJECTED"

        self.assertEqual(
            evaluation["result"],
            "SATISFIED",
        )
        self.assertNotEqual(
            evaluation["result"],
            admission,
        )

    def test_17_constraint_satisfaction_does_not_intrinsically_mean_acceptance(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "SATISFIED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "REJECTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "SATISFIED",
        )
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_18_constraint_violation_does_not_intrinsically_mean_rejection(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_19_admission_can_have_other_inputs(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "permission": "ALLOWED",
                "authority": "A1",
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_20_constraint_violation_is_not_permission(self):
        evaluation = {
            "result": "VIOLATED",
        }

        permission = "ALLOWED"

        self.assertNotEqual(
            evaluation["result"],
            permission,
        )

    def test_21_constraint_violation_is_not_authority(self):
        evaluation = {
            "result": "VIOLATED",
        }

        authority = "A1"

        self.assertNotEqual(
            evaluation["result"],
            authority,
        )

    def test_22_multiple_constraints_can_have_mixed_results(self):
        evaluations = [
            {
                "constraint": "identity_required",
                "result": "SATISFIED",
            },
            {
                "constraint": "state_required",
                "result": "VIOLATED",
            },
        ]

        self.assertEqual(
            evaluations[0]["result"],
            "SATISFIED",
        )
        self.assertEqual(
            evaluations[1]["result"],
            "VIOLATED",
        )

    def test_23_mixed_constraint_results_do_not_create_admission_automatically(self):
        evaluations = [
            {
                "constraint": "identity_required",
                "result": "SATISFIED",
            },
            {
                "constraint": "state_required",
                "result": "VIOLATED",
            },
        ]

        admission = None

        self.assertEqual(len(evaluations), 2)
        self.assertIsNone(admission)

    def test_24_final_boundary_violation_is_distinct_from_rejection(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        evaluation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        admission = evaluate_admission(
            {
                "constraint_result": evaluation["result"],
                "policy": "CUSTOM",
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            evaluation["result"],
            "VIOLATED",
        )
        self.assertEqual(
            admission,
            "ACCEPTED",
        )
        self.assertNotEqual(
            evaluation["result"],
            admission,
        )


if __name__ == "__main__":
    unittest.main()