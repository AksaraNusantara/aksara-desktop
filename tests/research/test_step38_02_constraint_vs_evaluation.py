import unittest


def make_constraint(name, rule):
    return {
        "name": name,
        "rule": rule,
    }


def evaluate_constraint(constraint, context):
    return context["result"]


class TestConstraintVsEvaluation(unittest.TestCase):

    def test_01_constraint_can_exist_without_evaluation(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        self.assertEqual(
            constraint["name"],
            "identity_required",
        )

    def test_02_evaluation_is_distinct_from_constraint(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        result = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        self.assertEqual(result, "SATISFIED")
        self.assertNotEqual(
            constraint["name"],
            result,
        )

    def test_03_same_constraint_can_have_different_results(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        result_a = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        result_b = evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertNotEqual(result_a, result_b)

    def test_04_result_change_does_not_mutate_constraint(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        original = dict(constraint)

        evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertEqual(
            constraint,
            original,
        )

    def test_05_constraint_is_not_result(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        result = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        self.assertEqual(
            constraint["rule"],
            "identity_must_exist",
        )
        self.assertEqual(
            result,
            "SATISFIED",
        )

    def test_06_result_does_not_become_constraint_identity(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        constraint_id = "C1"

        result = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        self.assertEqual(constraint_id, "C1")
        self.assertNotEqual(
            constraint_id,
            result,
        )

    def test_07_same_constraint_can_be_evaluated_in_multiple_contexts(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        contexts = [
            {"result": "SATISFIED"},
            {"result": "VIOLATED"},
        ]

        results = [
            evaluate_constraint(
                constraint,
                context,
            )
            for context in contexts
        ]

        self.assertEqual(
            results,
            ["SATISFIED", "VIOLATED"],
        )

    def test_08_context_changes_result_not_constraint(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        context_a = {
            "state": "ACTIVE",
            "result": "SATISFIED",
        }

        context_b = {
            "state": "INACTIVE",
            "result": "VIOLATED",
        }

        result_a = evaluate_constraint(
            constraint,
            context_a,
        )

        result_b = evaluate_constraint(
            constraint,
            context_b,
        )

        self.assertNotEqual(result_a, result_b)
        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )

    def test_09_policy_can_participate_in_constraint_evaluation(self):
        constraint = make_constraint(
            "request_required",
            "request_must_exist",
        )

        context = {
            "policy": "STRICT",
            "result": "SATISFIED",
        }

        result = evaluate_constraint(
            constraint,
            context,
        )

        self.assertEqual(
            context["policy"],
            "STRICT",
        )
        self.assertEqual(
            result,
            "SATISFIED",
        )

    def test_10_policy_is_distinct_from_constraint(self):
        constraint = make_constraint(
            "request_required",
            "request_must_exist",
        )

        context = {
            "policy": "STRICT",
            "result": "SATISFIED",
        }

        self.assertNotEqual(
            constraint["name"],
            context["policy"],
        )

    def test_11_policy_is_distinct_from_result(self):
        context = {
            "policy": "STRICT",
            "result": "SATISFIED",
        }

        self.assertNotEqual(
            context["policy"],
            context["result"],
        )

    def test_12_evaluation_is_contextual(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        result_a = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        result_b = evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertNotEqual(result_a, result_b)

    def test_13_constraint_remains_stable_across_evaluation(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        original_rule = constraint["rule"]

        for result in (
            "SATISFIED",
            "VIOLATED",
        ):
            evaluate_constraint(
                constraint,
                {"result": result},
            )

            self.assertEqual(
                constraint["rule"],
                original_rule,
            )

    def test_14_evaluation_does_not_change_constraint_identity(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        constraint_id = "C1"

        evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertEqual(constraint_id, "C1")
        self.assertEqual(
            constraint["name"],
            "identity_required",
        )

    def test_15_same_constraint_can_produce_multiple_observations(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        observations = [
            {
                "constraint": constraint,
                "result": "SATISFIED",
            },
            {
                "constraint": constraint,
                "result": "VIOLATED",
            },
        ]

        self.assertEqual(
            observations[0]["constraint"],
            observations[1]["constraint"],
        )
        self.assertNotEqual(
            observations[0]["result"],
            observations[1]["result"],
        )

    def test_16_evaluation_result_can_be_observation(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        observation = {
            "constraint": constraint,
            "result": "SATISFIED",
        }

        self.assertEqual(
            observation["constraint"],
            constraint,
        )
        self.assertEqual(
            observation["result"],
            "SATISFIED",
        )

    def test_17_evaluation_does_not_create_constraint_lifecycle(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        result = evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertEqual(result, "VIOLATED")
        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )

    def test_18_constraint_can_reference_multiple_inputs(self):
        constraint = make_constraint(
            "request_state",
            "request_exists_and_state_is_active",
        )

        context = {
            "request": "R1",
            "state": "ACTIVE",
            "result": "SATISFIED",
        }

        result = evaluate_constraint(
            constraint,
            context,
        )

        self.assertEqual(context["request"], "R1")
        self.assertEqual(context["state"], "ACTIVE")
        self.assertEqual(result, "SATISFIED")

    def test_19_constraint_rule_is_not_context_value(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        context = {
            "state": "ACTIVE",
            "result": "SATISFIED",
        }

        self.assertNotEqual(
            constraint["rule"],
            context["state"],
        )

    def test_20_violation_is_not_constraint_identity(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        result = evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertEqual(result, "VIOLATED")
        self.assertNotEqual(
            constraint["name"],
            result,
        )

    def test_21_constraint_and_result_can_be_composed_in_observation(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        observation = {
            "constraint": constraint,
            "result": "SATISFIED",
        }

        self.assertEqual(
            observation["constraint"]["name"],
            "identity_required",
        )
        self.assertEqual(
            observation["result"],
            "SATISFIED",
        )

    def test_22_multiple_constraints_can_have_independent_results(self):
        constraints = [
            make_constraint(
                "identity_required",
                "identity_must_exist",
            ),
            make_constraint(
                "state_required",
                "state_must_be_active",
            ),
        ]

        results = [
            "SATISFIED",
            "VIOLATED",
        ]

        self.assertEqual(len(constraints), 2)
        self.assertEqual(len(results), 2)
        self.assertNotEqual(
            constraints[0]["name"],
            constraints[1]["name"],
        )

    def test_23_result_does_not_replace_constraint_rule(self):
        constraint = make_constraint(
            "state_required",
            "state_must_be_active",
        )

        result = evaluate_constraint(
            constraint,
            {"result": "SATISFIED"},
        )

        self.assertEqual(
            constraint["rule"],
            "state_must_be_active",
        )
        self.assertEqual(
            result,
            "SATISFIED",
        )

    def test_24_constraint_evaluation_does_not_require_mutation(self):
        constraint = make_constraint(
            "request_required",
            "request_must_exist",
        )

        original_rule = constraint["rule"]

        evaluate_constraint(
            constraint,
            {"result": "VIOLATED"},
        )

        self.assertEqual(
            constraint["rule"],
            original_rule,
        )

    def test_25_final_boundary_constraint_is_not_evaluation_result(self):
        constraint = make_constraint(
            "identity_required",
            "identity_must_exist",
        )

        result = evaluate_constraint(
            constraint,
            {
                "policy": "STRICT",
                "result": "SATISFIED",
            },
        )

        self.assertEqual(
            constraint["name"],
            "identity_required",
        )
        self.assertEqual(
            result,
            "SATISFIED",
        )
        self.assertNotEqual(
            constraint["name"],
            result,
        )


if __name__ == "__main__":
    unittest.main()