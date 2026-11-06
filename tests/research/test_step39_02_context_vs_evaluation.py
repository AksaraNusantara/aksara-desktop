import unittest


def make_context(name, rule):
    return {
        "name": name,
        "rule": rule,
    }


def make_input(name, value):
    return {
        "name": name,
        "value": value,
    }


def evaluate(context, semantic_input, result):
    return {
        "context": context,
        "input": semantic_input,
        "result": result,
    }


class TestContextVsEvaluation(unittest.TestCase):

    def test_01_same_input_can_be_evaluated_in_different_contexts(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "active_is_allowed",
        )

        context_b = make_context(
            "context_b",
            "active_is_restricted",
        )

        result_a = evaluate(
            context_a,
            semantic_input,
            "ACCEPTED",
        )

        result_b = evaluate(
            context_b,
            semantic_input,
            "REJECTED",
        )

        self.assertEqual(
            result_a["input"],
            result_b["input"],
        )

    def test_02_different_contexts_can_produce_different_results(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "allow",
        )

        context_b = make_context(
            "context_b",
            "deny",
        )

        result_a = evaluate(
            context_a,
            semantic_input,
            "ACCEPTED",
        )

        result_b = evaluate(
            context_b,
            semantic_input,
            "REJECTED",
        )

        self.assertNotEqual(
            result_a["result"],
            result_b["result"],
        )

    def test_03_context_change_does_not_mutate_input(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "allow",
        )

        before = dict(semantic_input)

        evaluate(
            context_a,
            semantic_input,
            "ACCEPTED",
        )

        self.assertEqual(
            semantic_input,
            before,
        )

    def test_04_same_context_can_evaluate_multiple_inputs(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        inputs = [
            make_input("state", "ACTIVE"),
            make_input("permission", "ALLOWED"),
            make_input("identity", "REQ-001"),
        ]

        results = [
            evaluate(
                context,
                semantic_input,
                "VALID",
            )
            for semantic_input in inputs
        ]

        self.assertEqual(
            len(results),
            3,
        )

    def test_05_context_is_not_evaluation_result(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        result = evaluate(
            context,
            make_input("state", "ACTIVE"),
            "VALID",
        )

        self.assertNotEqual(
            context,
            result["result"],
        )

    def test_06_context_is_not_interpretation(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        interpretation = "STATE_IS_ACCEPTABLE"

        self.assertNotEqual(
            context["name"],
            interpretation,
        )

    def test_07_same_input_can_have_multiple_evaluation_observations(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observations = [
            evaluate(
                context_a,
                semantic_input,
                "VALID",
            ),
            evaluate(
                context_b,
                semantic_input,
                "INVALID",
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

    def test_08_evaluation_observations_do_not_mutate_each_other(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        observation_b = evaluate(
            context_b,
            semantic_input,
            "INVALID",
        )

        self.assertEqual(
            observation_a["result"],
            "VALID",
        )

        self.assertEqual(
            observation_b["result"],
            "INVALID",
        )

    def test_09_context_can_be_part_of_evaluation_input(self):
        context = make_context(
            "constraint_context",
            "strict",
        )

        semantic_input = make_input(
            "constraint",
            "state_required",
        )

        observation = evaluate(
            context,
            semantic_input,
            "VIOLATED",
        )

        self.assertIs(
            observation["context"],
            context,
        )

    def test_10_context_does_not_become_constraint(self):
        context = make_context(
            "constraint_context",
            "strict",
        )

        semantic_input = make_input(
            "constraint",
            "state_required",
        )

        observation = evaluate(
            context,
            semantic_input,
            "VIOLATED",
        )

        self.assertNotEqual(
            observation["context"]["name"],
            observation["input"]["name"],
        )

    def test_11_same_context_can_yield_different_results_for_different_inputs(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        input_a = make_input(
            "state",
            "ACTIVE",
        )

        input_b = make_input(
            "state",
            "INACTIVE",
        )

        result_a = evaluate(
            context,
            input_a,
            "VALID",
        )

        result_b = evaluate(
            context,
            input_b,
            "INVALID",
        )

        self.assertNotEqual(
            result_a["result"],
            result_b["result"],
        )

    def test_12_context_does_not_intrinsically_determine_result(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        result_a = evaluate(
            context,
            semantic_input,
            "VALID",
        )

        result_b = evaluate(
            context,
            semantic_input,
            "INVALID",
        )

        self.assertNotEqual(
            result_a["result"],
            result_b["result"],
        )

    def test_13_policy_like_context_can_change_result(self):
        semantic_input = make_input(
            "constraint",
            "state_required",
        )

        strict_context = make_context(
            "strict_policy",
            "violation_rejects",
        )

        lenient_context = make_context(
            "lenient_policy",
            "violation_allowed",
        )

        strict_result = evaluate(
            strict_context,
            semantic_input,
            "REJECTED",
        )

        lenient_result = evaluate(
            lenient_context,
            semantic_input,
            "ACCEPTED",
        )

        self.assertNotEqual(
            strict_result["result"],
            lenient_result["result"],
        )

    def test_14_context_change_does_not_change_input_identity(self):
        semantic_input = make_input(
            "identity",
            "REQ-001",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        identity_after_a = semantic_input["name"]

        evaluate(
            context_b,
            semantic_input,
            "VALID",
        )

        identity_after_b = semantic_input["name"]

        self.assertEqual(
            identity_after_a,
            identity_after_b,
        )

    def test_15_context_change_does_not_change_input_value(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        value_after_a = semantic_input["value"]

        evaluate(
            context_b,
            semantic_input,
            "INVALID",
        )

        value_after_b = semantic_input["value"]

        self.assertEqual(
            value_after_a,
            value_after_b,
        )

    def test_16_evaluation_result_belongs_to_observation_not_context(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        observation = evaluate(
            context,
            make_input("state", "ACTIVE"),
            "VALID",
        )

        self.assertEqual(
            observation["result"],
            "VALID",
        )

        self.assertNotIn(
            "result",
            context,
        )

    def test_17_context_can_be_shared_by_multiple_observations(self):
        context = make_context(
            "shared_context",
            "evaluate",
        )

        observations = [
            evaluate(
                context,
                make_input("state", "ACTIVE"),
                "VALID",
            ),
            evaluate(
                context,
                make_input("permission", "ALLOWED"),
                "VALID",
            ),
        ]

        self.assertIs(
            observations[0]["context"],
            observations[1]["context"],
        )

    def test_18_different_contexts_can_reference_same_input_without_copying_it(self):
        semantic_input = make_input(
            "identity",
            "REQ-001",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        observation_b = evaluate(
            context_b,
            semantic_input,
            "INVALID",
        )

        self.assertIs(
            observation_a["input"],
            observation_b["input"],
        )

    def test_19_context_is_not_state(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        states = {
            "ACTIVE",
            "INACTIVE",
        }

        self.assertNotIn(
            context["name"],
            states,
        )

    def test_20_context_is_not_permission(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        permissions = {
            "ALLOWED",
            "DENIED",
        }

        self.assertNotIn(
            context["name"],
            permissions,
        )

    def test_21_context_is_not_authority(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        authority = "AUTH-001"

        self.assertNotEqual(
            context["name"],
            authority,
        )

    def test_22_context_is_not_admission_decision(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        decisions = {
            "ACCEPTED",
            "REJECTED",
        }

        self.assertNotIn(
            context["name"],
            decisions,
        )

    def test_23_context_change_can_create_new_evaluation_observation(self):
        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        observation_b = evaluate(
            context_b,
            semantic_input,
            "INVALID",
        )

        self.assertIsNot(
            observation_a,
            observation_b,
        )

    def test_24_new_observation_does_not_imply_new_input_identity(self):
        semantic_input = make_input(
            "identity",
            "REQ-001",
        )

        context_a = make_context(
            "context_a",
            "rule_a",
        )

        context_b = make_context(
            "context_b",
            "rule_b",
        )

        observation_a = evaluate(
            context_a,
            semantic_input,
            "VALID",
        )

        observation_b = evaluate(
            context_b,
            semantic_input,
            "INVALID",
        )

        self.assertIs(
            observation_a["input"],
            observation_b["input"],
        )

    def test_25_context_is_semantic_frame_not_evaluation_result(self):
        context = make_context(
            "execution_context",
            "evaluate",
        )

        semantic_input = make_input(
            "state",
            "ACTIVE",
        )

        observation = evaluate(
            context,
            semantic_input,
            "VALID",
        )

        self.assertEqual(
            observation["context"]["purpose"]
            if "purpose" in observation["context"]
            else observation["context"]["rule"],
            "evaluate",
        )


if __name__ == "__main__":
    unittest.main()