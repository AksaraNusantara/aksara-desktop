import unittest


class TestContextCompositionVsEvaluation(unittest.TestCase):

    def test_01_multiple_contexts_can_be_used_in_one_evaluation(self):
        contexts = ["context_a", "context_b"]

        evaluation_input = {
            "contexts": contexts,
            "subject": "input_x",
        }

        self.assertIn("context_a", evaluation_input["contexts"])
        self.assertIn("context_b", evaluation_input["contexts"])

    def test_02_context_composition_is_not_evaluation(self):
        composition = ["context_a", "context_b"]
        evaluation = {
            "input": composition,
            "result": "accepted",
        }

        self.assertIsNot(composition, evaluation)

    def test_03_composition_can_exist_without_evaluation(self):
        composition = ["context_a", "context_b"]

        self.assertIsNotNone(composition)

    def test_04_evaluation_can_exist_without_composite_context(self):
        evaluation = {
            "contexts": ["context_a", "context_b"],
            "result": "accepted",
        }

        self.assertEqual(
            evaluation["contexts"],
            ["context_a", "context_b"],
        )

    def test_05_same_context_composition_can_be_used_in_multiple_evaluations(self):
        composition = ["context_a", "context_b"]

        evaluation_a = {
            "input": composition,
            "result": "accepted",
        }

        evaluation_b = {
            "input": composition,
            "result": "rejected",
        }

        self.assertEqual(evaluation_a["input"], evaluation_b["input"])
        self.assertNotEqual(
            evaluation_a["result"],
            evaluation_b["result"],
        )

    def test_06_different_compositions_can_produce_different_results(self):
        composition_a = ["context_a"]
        composition_b = ["context_b"]

        evaluation_a = {
            "input": composition_a,
            "result": "accepted",
        }

        evaluation_b = {
            "input": composition_b,
            "result": "rejected",
        }

        self.assertNotEqual(
            evaluation_a["result"],
            evaluation_b["result"],
        )

    def test_07_composition_does_not_intrinsically_determine_result(self):
        composition = ["context_a", "context_b"]

        evaluation_1 = {
            "input": composition,
            "result": "accepted",
        }

        evaluation_2 = {
            "input": composition,
            "result": "rejected",
        }

        self.assertEqual(evaluation_1["input"], evaluation_2["input"])
        self.assertNotEqual(
            evaluation_1["result"],
            evaluation_2["result"],
        )

    def test_08_context_order_can_be_semantically_preserved(self):
        composition = ["context_a", "context_b"]

        self.assertEqual(
            composition,
            ["context_a", "context_b"],
        )

    def test_09_reordering_contexts_changes_composition_representation(self):
        composition_a = ["context_a", "context_b"]
        composition_b = ["context_b", "context_a"]

        self.assertNotEqual(composition_a, composition_b)

    def test_10_reordering_does_not_change_context_identity(self):
        composition_a = ["context_a", "context_b"]
        composition_b = ["context_b", "context_a"]

        self.assertEqual(set(composition_a), set(composition_b))

    def test_11_evaluation_result_belongs_to_observation_not_context(self):
        context = "context_a"

        observation = {
            "context": context,
            "result": "accepted",
        }

        self.assertEqual(observation["context"], context)
        self.assertEqual(observation["result"], "accepted")

    def test_12_same_context_can_participate_in_multiple_observations(self):
        context = "context_a"

        observation_a = {
            "context": context,
            "result": "accepted",
        }

        observation_b = {
            "context": context,
            "result": "rejected",
        }

        self.assertEqual(
            observation_a["context"],
            observation_b["context"],
        )

    def test_13_composition_can_be_shared_by_multiple_observations(self):
        composition = ["context_a", "context_b"]

        observation_a = {
            "composition": composition,
            "result": "accepted",
        }

        observation_b = {
            "composition": composition,
            "result": "rejected",
        }

        self.assertEqual(
            observation_a["composition"],
            observation_b["composition"],
        )

    def test_14_evaluation_observation_does_not_mutate_composition(self):
        composition = ["context_a", "context_b"]

        evaluation = {
            "composition": composition,
            "result": "accepted",
        }

        self.assertEqual(
            evaluation["composition"],
            ["context_a", "context_b"],
        )

    def test_15_different_results_do_not_require_context_identity_change(self):
        context = "context_a"

        observation_a = {
            "context": context,
            "result": "accepted",
        }

        observation_b = {
            "context": context,
            "result": "rejected",
        }

        self.assertEqual(
            observation_a["context"],
            observation_b["context"],
        )

    def test_16_context_composition_is_distinct_from_evaluation_result(self):
        composition = ["context_a", "context_b"]
        result = "accepted"

        self.assertIsNot(composition, result)

    def test_17_context_composition_can_be_an_evaluation_input(self):
        composition = ["context_a", "context_b"]

        evaluation = {
            "contexts": composition,
            "subject": "input_x",
        }

        self.assertEqual(
            evaluation["contexts"],
            composition,
        )

    def test_18_context_composition_does_not_become_constraint(self):
        composition = ["context_a", "context_b"]

        constraint = {
            "type": "require_all",
            "contexts": composition,
        }

        self.assertIsNot(composition, constraint)

    def test_19_same_contexts_can_support_different_subjects(self):
        composition = ["context_a", "context_b"]

        evaluation_a = {
            "contexts": composition,
            "subject": "input_x",
            "result": "accepted",
        }

        evaluation_b = {
            "contexts": composition,
            "subject": "input_y",
            "result": "rejected",
        }

        self.assertEqual(
            evaluation_a["contexts"],
            evaluation_b["contexts"],
        )
        self.assertNotEqual(
            evaluation_a["subject"],
            evaluation_b["subject"],
        )

    def test_20_same_composition_can_support_multiple_evaluation_results(self):
        composition = ["context_a", "context_b"]

        results = [
            {"composition": composition, "result": "accepted"},
            {"composition": composition, "result": "rejected"},
        ]

        self.assertEqual(
            results[0]["composition"],
            results[1]["composition"],
        )
        self.assertNotEqual(
            results[0]["result"],
            results[1]["result"],
        )

    def test_21_composition_does_not_create_evaluation_lifecycle(self):
        composition = ["context_a", "context_b"]

        self.assertIsInstance(composition, list)

    def test_22_evaluation_result_does_not_change_context_identity(self):
        composition = ["context_a", "context_b"]

        observation = {
            "composition": composition,
            "result": "accepted",
        }

        self.assertEqual(
            observation["composition"],
            ["context_a", "context_b"],
        )

    def test_23_context_composition_does_not_require_new_evaluation_identity(self):
        composition = ["context_a", "context_b"]

        evaluation = {
            "contexts": composition,
            "result": "accepted",
        }

        self.assertNotIn("evaluation_id", evaluation)

    def test_24_new_evaluation_observation_does_not_require_new_context_identity(self):
        composition = ["context_a", "context_b"]

        observation_a = {
            "contexts": composition,
            "result": "accepted",
        }

        observation_b = {
            "contexts": composition,
            "result": "rejected",
        }

        self.assertEqual(
            observation_a["contexts"],
            observation_b["contexts"],
        )

    def test_25_final_boundary_composition_is_not_evaluation(self):
        composition = ["context_a", "context_b"]

        evaluation = {
            "contexts": composition,
            "result": "accepted",
        }

        self.assertIsNot(composition, evaluation)
        self.assertNotEqual(
            type(composition),
            type(evaluation),
        )


if __name__ == "__main__":
    unittest.main()