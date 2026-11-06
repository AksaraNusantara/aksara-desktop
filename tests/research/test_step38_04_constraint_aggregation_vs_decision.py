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


def aggregate_results(observations):
    return [observation["result"] for observation in observations]


def evaluate_admission(inputs):
    return inputs["admission_result"]


class TestConstraintAggregationVsDecision(unittest.TestCase):

    def test_01_multiple_constraint_results_can_coexist(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "SATISFIED",
            ),
        ]

        self.assertEqual(len(observations), 2)
        self.assertEqual(
            observations[0]["result"],
            "SATISFIED",
        )
        self.assertEqual(
            observations[1]["result"],
            "SATISFIED",
        )

    def test_02_aggregation_is_distinct_from_individual_constraint_result(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertNotEqual(
            aggregated,
            observations[0]["result"],
        )

    def test_03_aggregation_is_not_admission_decision(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)
        admission = "REJECTED"

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertNotEqual(
            aggregated,
            admission,
        )

    def test_04_same_aggregation_can_participate_in_different_decisions(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        result_a = evaluate_admission(
            {
                "constraint_results": aggregated,
                "admission_result": "REJECTED",
            }
        )

        result_b = evaluate_admission(
            {
                "constraint_results": aggregated,
                "admission_result": "ACCEPTED",
            }
        )

        self.assertNotEqual(
            result_a,
            result_b,
        )

    def test_05_all_satisfied_does_not_intrinsically_mean_acceptance(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "SATISFIED",
            ),
        ]

        aggregated = aggregate_results(observations)

        admission = evaluate_admission(
            {
                "constraint_results": aggregated,
                "admission_result": "REJECTED",
            }
        )

        self.assertEqual(
            aggregated,
            ["SATISFIED", "SATISFIED"],
        )
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_06_any_violation_does_not_intrinsically_mean_rejection(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        admission = evaluate_admission(
            {
                "constraint_results": aggregated,
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_07_policy_can_change_interpretation_of_same_aggregation(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        strict = evaluate_admission(
            {
                "constraint_results": aggregated,
                "policy": "STRICT",
                "admission_result": "REJECTED",
            }
        )

        lenient = evaluate_admission(
            {
                "constraint_results": aggregated,
                "policy": "LENIENT",
                "admission_result": "ACCEPTED",
            }
        )

        self.assertNotEqual(strict, lenient)

    def test_08_aggregation_does_not_mutate_observations(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        original = [dict(item) for item in observations]

        aggregate_results(observations)

        self.assertEqual(
            observations,
            original,
        )

    def test_09_aggregation_does_not_change_constraint_identity(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        observation = evaluate_constraint(
            constraint,
            "VIOLATED",
        )

        aggregate_results([observation])

        self.assertEqual(
            constraint["name"],
            "state_required",
        )

    def test_10_aggregation_does_not_create_composite_constraint_identity(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        composite = (
            observations[0]["constraint"]["name"],
            observations[1]["constraint"]["name"],
        )

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertNotEqual(
            composite,
            observations[0]["constraint"]["name"],
        )

    def test_11_aggregation_can_be_observed_separately(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregation = {
            "results": aggregate_results(observations),
        }

        self.assertEqual(
            aggregation["results"],
            ["SATISFIED", "VIOLATED"],
        )

    def test_12_aggregation_does_not_require_admission(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)
        admission = None

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertIsNone(admission)

    def test_13_multiple_constraint_sets_can_exist_for_same_request(self):
        set_a = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
        ]

        set_b = [
            evaluate_constraint(
                make_constraint(
                    "permission_required",
                    "permission_must_exist",
                ),
                "VIOLATED",
            ),
        ]

        self.assertNotEqual(
            set_a[0]["constraint"]["name"],
            set_b[0]["constraint"]["name"],
        )

    def test_14_constraint_set_identity_is_not_admission_identity(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "SATISFIED",
            ),
        ]

        constraint_set_id = "CS-1"
        admission_id = "A-1"

        self.assertNotEqual(
            constraint_set_id,
            admission_id,
        )
        self.assertEqual(
            len(observations),
            2,
        )

    def test_15_mixed_results_remain_mixed_results(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
            evaluate_constraint(
                make_constraint(
                    "permission_required",
                    "permission_must_exist",
                ),
                "SATISFIED",
            ),
        ]

        aggregated = aggregate_results(observations)

        self.assertEqual(
            aggregated,
            [
                "SATISFIED",
                "VIOLATED",
                "SATISFIED",
            ],
        )

    def test_16_aggregation_result_is_not_state(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        states = {
            "ACTIVE",
            "INACTIVE",
        }

        self.assertTrue(
            all(
                result not in states
                for result in aggregated
            )
        )

    def test_17_aggregation_result_is_not_permission(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "permission_required",
                    "permission_must_exist",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        permissions = {
            "ALLOWED",
            "DENIED",
        }

        self.assertTrue(
            all(
                result not in permissions
                for result in aggregated
            )
        )

    def test_18_aggregation_result_is_not_authority(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "authority_required",
                    "authority_must_exist",
                ),
                "SATISFIED",
            ),
        ]

        aggregated = aggregate_results(observations)

        authority = "A1"

        self.assertNotEqual(
            aggregated,
            authority,
        )

    def test_19_aggregation_can_be_input_to_admission_without_becoming_admission(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        admission = evaluate_admission(
            {
                "constraint_results": aggregated,
                "other_input": "PERMISSION_ALLOWED",
                "admission_result": "ACCEPTED",
            }
        )

        self.assertEqual(
            admission,
            "ACCEPTED",
        )
        self.assertNotEqual(
            aggregated,
            admission,
        )

    def test_20_aggregation_does_not_create_lifecycle(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        self.assertEqual(
            aggregated,
            ["VIOLATED"],
        )

    def test_21_order_of_constraint_results_can_remain_semantically_distinct(self):
        observations_a = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        observations_b = list(reversed(observations_a))

        aggregation_a = aggregate_results(observations_a)
        aggregation_b = aggregate_results(observations_b)

        self.assertNotEqual(
            aggregation_a,
            aggregation_b,
        )

    def test_22_same_results_can_belong_to_different_constraint_sets(self):
        set_a = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
        ]

        set_b = [
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "SATISFIED",
            ),
        ]

        aggregation_a = aggregate_results(set_a)
        aggregation_b = aggregate_results(set_b)

        self.assertEqual(
            aggregation_a,
            aggregation_b,
        )
        self.assertNotEqual(
            set_a[0]["constraint"]["name"],
            set_b[0]["constraint"]["name"],
        )

    def test_23_final_boundary_aggregation_is_not_admission_decision(self):
        observations = [
            evaluate_constraint(
                make_constraint(
                    "identity_required",
                    "identity_must_exist",
                ),
                "SATISFIED",
            ),
            evaluate_constraint(
                make_constraint(
                    "state_required",
                    "state_must_be_active",
                ),
                "VIOLATED",
            ),
        ]

        aggregated = aggregate_results(observations)

        admission = evaluate_admission(
            {
                "constraint_results": aggregated,
                "policy": "CUSTOM",
                "admission_result": "REJECTED",
            }
        )

        self.assertEqual(
            aggregated,
            ["SATISFIED", "VIOLATED"],
        )
        self.assertEqual(
            admission,
            "REJECTED",
        )
        self.assertNotEqual(
            aggregated,
            admission,
        )


if __name__ == "__main__":
    unittest.main()