import unittest


class TestContextCompositionVsDecision(unittest.TestCase):

    def test_01_multiple_contexts_can_be_used_in_one_decision_evaluation(self):
        contexts = ["context_a", "context_b"]

        decision_evaluation = {
            "contexts": contexts,
            "subject": "input_x",
        }

        self.assertIn("context_a", decision_evaluation["contexts"])
        self.assertIn("context_b", decision_evaluation["contexts"])

    def test_02_context_composition_is_not_decision(self):
        composition = ["context_a", "context_b"]

        decision = {
            "contexts": composition,
            "value": "proceed",
        }

        self.assertIsNot(composition, decision)

    def test_03_composition_can_exist_without_decision(self):
        composition = ["context_a", "context_b"]

        self.assertIsNotNone(composition)

    def test_04_decision_can_exist_without_composite_context(self):
        decision = {
            "contexts": ["context_a", "context_b"],
            "value": "proceed",
        }

        self.assertEqual(
            decision["contexts"],
            ["context_a", "context_b"],
        )

    def test_05_same_composition_can_support_multiple_decisions(self):
        composition = ["context_a", "context_b"]

        decision_a = {
            "contexts": composition,
            "value": "proceed",
        }

        decision_b = {
            "contexts": composition,
            "value": "defer",
        }

        self.assertEqual(
            decision_a["contexts"],
            decision_b["contexts"],
        )

        self.assertNotEqual(
            decision_a["value"],
            decision_b["value"],
        )

    def test_06_different_compositions_can_support_different_decisions(self):
        composition_a = ["context_a"]
        composition_b = ["context_b"]

        decision_a = {
            "contexts": composition_a,
            "value": "proceed",
        }

        decision_b = {
            "contexts": composition_b,
            "value": "reject",
        }

        self.assertNotEqual(
            decision_a["value"],
            decision_b["value"],
        )

    def test_07_composition_does_not_intrinsically_determine_decision(self):
        composition = ["context_a", "context_b"]

        decision_a = {
            "contexts": composition,
            "value": "proceed",
        }

        decision_b = {
            "contexts": composition,
            "value": "reject",
        }

        self.assertEqual(
            decision_a["contexts"],
            decision_b["contexts"],
        )

        self.assertNotEqual(
            decision_a["value"],
            decision_b["value"],
        )

    def test_08_context_order_can_be_preserved_in_decision_input(self):
        composition = ["context_a", "context_b"]

        decision_evaluation = {
            "contexts": composition,
        }

        self.assertEqual(
            decision_evaluation["contexts"],
            ["context_a", "context_b"],
        )

    def test_09_reordering_contexts_changes_composition_representation(self):
        composition_a = ["context_a", "context_b"]
        composition_b = ["context_b", "context_a"]

        self.assertNotEqual(
            composition_a,
            composition_b,
        )

    def test_10_reordering_does_not_change_context_identity(self):
        composition_a = ["context_a", "context_b"]
        composition_b = ["context_b", "context_a"]

        self.assertEqual(
            set(composition_a),
            set(composition_b),
        )

    def test_11_decision_value_belongs_to_decision_observation_not_context(self):
        context = "context_a"

        observation = {
            "context": context,
            "decision": "proceed",
        }

        self.assertEqual(
            observation["context"],
            context,
        )

        self.assertEqual(
            observation["decision"],
            "proceed",
        )

    def test_12_same_context_can_participate_in_multiple_decision_observations(self):
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

    def test_13_composition_can_be_shared_by_multiple_decision_observations(self):
        composition = ["context_a", "context_b"]

        observation_a = {
            "composition": composition,
            "decision": "proceed",
        }

        observation_b = {
            "composition": composition,
            "decision": "reject",
        }

        self.assertEqual(
            observation_a["composition"],
            observation_b["composition"],
        )

    def test_14_decision_observation_does_not_mutate_composition(self):
        composition = ["context_a", "context_b"]

        observation = {
            "composition": composition,
            "decision": "proceed",
        }

        self.assertEqual(
            observation["composition"],
            ["context_a", "context_b"],
        )

    def test_15_different_decisions_do_not_require_context_identity_change(self):
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

    def test_16_context_composition_is_distinct_from_decision_value(self):
        composition = ["context_a", "context_b"]
        decision = "proceed"

        self.assertIsNot(
            composition,
            decision,
        )

    def test_17_context_composition_can_be_a_decision_input(self):
        composition = ["context_a", "context_b"]

        decision_evaluation = {
            "contexts": composition,
            "subject": "input_x",
        }

        self.assertEqual(
            decision_evaluation["contexts"],
            composition,
        )

    def test_18_context_composition_does_not_become_permission(self):
        composition = ["context_a", "context_b"]

        permission = {
            "contexts": composition,
            "allowed": True,
        }

        self.assertIsNot(
            composition,
            permission,
        )

    def test_19_same_contexts_can_support_different_subject_decisions(self):
        composition = ["context_a", "context_b"]

        decision_a = {
            "contexts": composition,
            "subject": "input_x",
            "value": "proceed",
        }

        decision_b = {
            "contexts": composition,
            "subject": "input_y",
            "value": "reject",
        }

        self.assertEqual(
            decision_a["contexts"],
            decision_b["contexts"],
        )

        self.assertNotEqual(
            decision_a["subject"],
            decision_b["subject"],
        )

    def test_20_same_composition_can_support_multiple_decision_values(self):
        composition = ["context_a", "context_b"]

        decisions = [
            {
                "composition": composition,
                "value": "proceed",
            },
            {
                "composition": composition,
                "value": "reject",
            },
        ]

        self.assertEqual(
            decisions[0]["composition"],
            decisions[1]["composition"],
        )

        self.assertNotEqual(
            decisions[0]["value"],
            decisions[1]["value"],
        )

    def test_21_composition_does_not_create_decision_lifecycle(self):
        composition = ["context_a", "context_b"]

        self.assertIsInstance(
            composition,
            list,
        )

    def test_22_decision_value_does_not_change_context_identity(self):
        composition = ["context_a", "context_b"]

        observation = {
            "composition": composition,
            "decision": "proceed",
        }

        self.assertEqual(
            observation["composition"],
            ["context_a", "context_b"],
        )

    def test_23_context_composition_does_not_require_new_decision_identity(self):
        composition = ["context_a", "context_b"]

        decision = {
            "contexts": composition,
            "value": "proceed",
        }

        self.assertNotIn(
            "decision_id",
            decision,
        )

    def test_24_new_decision_observation_does_not_require_new_context_identity(self):
        composition = ["context_a", "context_b"]

        observation_a = {
            "contexts": composition,
            "decision": "proceed",
        }

        observation_b = {
            "contexts": composition,
            "decision": "reject",
        }

        self.assertEqual(
            observation_a["contexts"],
            observation_b["contexts"],
        )

    def test_25_final_boundary_composition_is_not_decision(self):
        composition = ["context_a", "context_b"]

        decision = {
            "contexts": composition,
            "value": "proceed",
        }

        self.assertIsNot(
            composition,
            decision,
        )

        self.assertNotEqual(
            type(composition),
            type(decision),
        )


if __name__ == "__main__":
    unittest.main()