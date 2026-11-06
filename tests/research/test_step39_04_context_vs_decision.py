import unittest


class TestContextVsDecision(unittest.TestCase):

    def test_01_context_can_be_input_to_decision_evaluation(self):
        context = "context_a"

        evaluation = {
            "context": context,
            "subject": "input_x",
        }

        self.assertEqual(evaluation["context"], context)

    def test_02_context_is_not_decision(self):
        context = "context_a"

        decision = {
            "value": "proceed",
        }

        self.assertIsNot(context, decision)

    def test_03_same_input_can_produce_different_decisions_in_different_contexts(self):
        input_value = "input_x"

        decision_a = {
            "context": "context_a",
            "input": input_value,
            "decision": "proceed",
        }

        decision_b = {
            "context": "context_b",
            "input": input_value,
            "decision": "reject",
        }

        self.assertEqual(
            decision_a["input"],
            decision_b["input"],
        )

        self.assertNotEqual(
            decision_a["decision"],
            decision_b["decision"],
        )

    def test_04_context_change_does_not_mutate_input(self):
        input_value = {
            "id": "input_x",
            "value": "sample",
        }

        original = input_value.copy()

        _decision = {
            "context": "context_a",
            "input": input_value,
            "decision": "proceed",
        }

        self.assertEqual(input_value, original)

    def test_05_context_does_not_intrinsically_determine_decision(self):
        context = "context_a"

        decision_a = {
            "context": context,
            "decision": "proceed",
        }

        decision_b = {
            "context": context,
            "decision": "reject",
        }

        self.assertEqual(
            decision_a["context"],
            decision_b["context"],
        )

        self.assertNotEqual(
            decision_a["decision"],
            decision_b["decision"],
        )

    def test_06_policy_context_can_change_decision(self):
        context_a = {
            "policy": "policy_a",
        }

        context_b = {
            "policy": "policy_b",
        }

        decision_a = {
            "context": context_a,
            "decision": "proceed",
        }

        decision_b = {
            "context": context_b,
            "decision": "reject",
        }

        self.assertNotEqual(
            decision_a["decision"],
            decision_b["decision"],
        )

    def test_07_context_is_not_admission_decision(self):
        context = "context_a"

        admission = {
            "decision": "accepted",
        }

        self.assertIsNot(context, admission)

    def test_08_context_is_not_permission(self):
        context = "context_a"

        permission = {
            "allowed": True,
        }

        self.assertIsNot(context, permission)

    def test_09_context_is_not_authority(self):
        context = "context_a"

        authority = {
            "name": "authority_a",
        }

        self.assertIsNot(context, authority)

    def test_10_context_is_not_execution(self):
        context = "context_a"

        execution = {
            "state": "executed",
        }

        self.assertIsNot(context, execution)

    def test_11_same_context_can_be_shared_by_multiple_decision_observations(self):
        context = "context_a"

        observation_a = {
            "context": context,
            "decision": "proceed",
        }

        observation_b = {
            "context": context,
            "decision": "reject",
        }

        self.assertEqual(
            observation_a["context"],
            observation_b["context"],
        )

    def test_12_same_input_can_have_multiple_contextual_decisions(self):
        input_value = "input_x"

        observations = [
            {
                "input": input_value,
                "context": "context_a",
                "decision": "proceed",
            },
            {
                "input": input_value,
                "context": "context_b",
                "decision": "reject",
            },
        ]

        self.assertEqual(
            observations[0]["input"],
            observations[1]["input"],
        )

    def test_13_context_change_can_create_new_decision_observation(self):
        input_value = "input_x"

        observation_a = {
            "input": input_value,
            "context": "context_a",
            "decision": "proceed",
        }

        observation_b = {
            "input": input_value,
            "context": "context_b",
            "decision": "reject",
        }

        self.assertNotEqual(
            observation_a["context"],
            observation_b["context"],
        )

    def test_14_new_decision_observation_does_not_require_new_input_identity(self):
        input_id = "input_x"

        observation_a = {
            "input_id": input_id,
            "context": "context_a",
            "decision": "proceed",
        }

        observation_b = {
            "input_id": input_id,
            "context": "context_b",
            "decision": "reject",
        }

        self.assertEqual(
            observation_a["input_id"],
            observation_b["input_id"],
        )

    def test_15_context_can_exist_without_decision(self):
        context = {
            "name": "context_a",
        }

        self.assertIsNotNone(context)

    def test_16_decision_can_be_observed_without_mutating_context(self):
        context = {
            "name": "context_a",
        }

        original = context.copy()

        _observation = {
            "context": context,
            "decision": "proceed",
        }

        self.assertEqual(context, original)

    def test_17_same_context_can_produce_different_decisions_for_different_inputs(self):
        context = "context_a"

        decision_a = {
            "context": context,
            "input": "input_a",
            "decision": "proceed",
        }

        decision_b = {
            "context": context,
            "input": "input_b",
            "decision": "reject",
        }

        self.assertEqual(
            decision_a["context"],
            decision_b["context"],
        )

        self.assertNotEqual(
            decision_a["input"],
            decision_b["input"],
        )

    def test_18_context_does_not_become_constraint(self):
        context = "context_a"

        constraint = {
            "type": "required",
        }

        self.assertIsNot(context, constraint)

    def test_19_context_does_not_become_evaluation_result(self):
        context = "context_a"

        result = {
            "value": True,
        }

        self.assertIsNot(context, result)

    def test_20_context_identity_can_remain_stable_across_decisions(self):
        context_id = "context_a"

        decision_a = {
            "context_id": context_id,
            "decision": "proceed",
        }

        decision_b = {
            "context_id": context_id,
            "decision": "reject",
        }

        self.assertEqual(
            decision_a["context_id"],
            decision_b["context_id"],
        )

    def test_21_context_change_does_not_require_context_mutation(self):
        context_a = {
            "id": "context_a",
        }

        context_b = {
            "id": "context_b",
        }

        self.assertNotEqual(
            context_a["id"],
            context_b["id"],
        )

    def test_22_different_contexts_can_reference_same_input(self):
        input_id = "input_x"

        observation_a = {
            "context": "context_a",
            "input_id": input_id,
        }

        observation_b = {
            "context": "context_b",
            "input_id": input_id,
        }

        self.assertEqual(
            observation_a["input_id"],
            observation_b["input_id"],
        )

    def test_23_context_change_can_change_decision_without_input_mutation(self):
        input_value = {
            "id": "input_x",
            "value": "sample",
        }

        original = input_value.copy()

        observation_a = {
            "context": "context_a",
            "input": input_value,
            "decision": "proceed",
        }

        observation_b = {
            "context": "context_b",
            "input": input_value,
            "decision": "reject",
        }

        self.assertEqual(
            observation_a["input"],
            observation_b["input"],
        )

        self.assertEqual(
            input_value,
            original,
        )

    def test_24_context_composition_is_not_decision(self):
        contexts = ["context_a", "context_b"]

        decision = {
            "contexts": contexts,
            "decision": "proceed",
        }

        self.assertIsNot(contexts, decision)

    def test_25_final_boundary_context_is_not_decision(self):
        context = "context_a"

        decision = {
            "context": context,
            "decision": "proceed",
        }

        self.assertIsNot(context, decision)


if __name__ == "__main__":
    unittest.main()