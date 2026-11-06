import unittest


def make_relationship(source, target, relation):
    return {
        "source": source,
        "target": target,
        "relation": relation,
    }


def evaluate_relationship(relationship, context):
    return context["result"]


class TestRelationshipVsInterpretation(unittest.TestCase):

    def test_01_relationship_can_exist_without_evaluation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        self.assertEqual(
            relationship["source"],
            "request",
        )
        self.assertEqual(
            relationship["target"],
            "decision",
        )
        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )

    def test_02_evaluation_is_distinct_from_relationship(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context = {
            "result": "APPLICABLE",
        }

        result = evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(result, "APPLICABLE")
        self.assertNotEqual(
            result,
            relationship["relation"],
        )

    def test_03_same_relationship_can_have_different_evaluation_results(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context_a = {
            "result": "APPLICABLE",
        }

        context_b = {
            "result": "NOT_APPLICABLE",
        }

        result_a = evaluate_relationship(
            relationship,
            context_a,
        )

        result_b = evaluate_relationship(
            relationship,
            context_b,
        )

        self.assertNotEqual(result_a, result_b)

    def test_04_evaluation_change_does_not_change_relationship(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        original_relationship = dict(relationship)

        context = {
            "result": "APPLICABLE",
        }

        evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(
            relationship,
            original_relationship,
        )

    def test_05_relationship_does_not_become_evaluation_result(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context = {
            "result": "APPLICABLE",
        }

        result = evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(result, "APPLICABLE")

    def test_06_evaluation_does_not_become_relationship_identity(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        relationship_id = "REL-1"

        context = {
            "result": "APPLICABLE",
        }

        result = evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(relationship_id, "REL-1")
        self.assertEqual(result, "APPLICABLE")
        self.assertNotEqual(
            relationship_id,
            result,
        )

    def test_07_same_relationship_can_be_evaluated_in_multiple_contexts(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        contexts = [
            {"result": "APPLICABLE"},
            {"result": "NOT_APPLICABLE"},
        ]

        results = [
            evaluate_relationship(
                relationship,
                context,
            )
            for context in contexts
        ]

        self.assertEqual(
            results,
            ["APPLICABLE", "NOT_APPLICABLE"],
        )

    def test_08_context_changes_evaluation_not_relationship(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context_a = {
            "result": "APPLICABLE",
        }

        context_b = {
            "result": "NOT_APPLICABLE",
        }

        result_a = evaluate_relationship(
            relationship,
            context_a,
        )

        result_b = evaluate_relationship(
            relationship,
            context_b,
        )

        self.assertNotEqual(result_a, result_b)
        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )

    def test_09_policy_can_participate_in_interpretation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context = {
            "policy": "STRICT",
            "result": "NOT_APPLICABLE",
        }

        result = evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(
            context["policy"],
            "STRICT",
        )
        self.assertEqual(
            result,
            "NOT_APPLICABLE",
        )

    def test_10_policy_is_distinct_from_relationship(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context = {
            "policy": "STRICT",
            "result": "NOT_APPLICABLE",
        }

        self.assertNotEqual(
            relationship["relation"],
            context["policy"],
        )

    def test_11_policy_is_distinct_from_evaluation_result(self):
        context = {
            "policy": "STRICT",
            "result": "APPLICABLE",
        }

        self.assertNotEqual(
            context["policy"],
            context["result"],
        )

    def test_12_evaluation_is_contextual(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        context_a = {
            "result": "APPLICABLE",
        }

        context_b = {
            "result": "NOT_APPLICABLE",
        }

        self.assertNotEqual(
            evaluate_relationship(relationship, context_a),
            evaluate_relationship(relationship, context_b),
        )

    def test_13_relationship_remains_stable_across_evaluation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        original_relation = relationship["relation"]

        for result in (
            "APPLICABLE",
            "NOT_APPLICABLE",
            "ALLOWED",
            "NOT_ALLOWED",
        ):
            context = {"result": result}

            evaluate_relationship(
                relationship,
                context,
            )

            self.assertEqual(
                relationship["relation"],
                original_relation,
            )

    def test_14_evaluation_does_not_change_endpoint_identity(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        request_id = "R1"
        decision_id = "D1"

        context = {
            "result": "APPLICABLE",
        }

        evaluate_relationship(
            relationship,
            context,
        )

        self.assertEqual(request_id, "R1")
        self.assertEqual(decision_id, "D1")

    def test_15_same_endpoints_can_produce_different_results(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result_a = evaluate_relationship(
            relationship,
            {"result": "ALLOWED"},
        )

        result_b = evaluate_relationship(
            relationship,
            {"result": "NOT_ALLOWED"},
        )

        self.assertNotEqual(result_a, result_b)

    def test_16_relationship_does_not_determine_result_intrinsically(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result_a = evaluate_relationship(
            relationship,
            {"result": "APPLICABLE"},
        )

        result_b = evaluate_relationship(
            relationship,
            {"result": "NOT_APPLICABLE"},
        )

        self.assertNotEqual(result_a, result_b)

    def test_17_evaluation_result_is_not_relationship_state(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result = evaluate_relationship(
            relationship,
            {"result": "APPLICABLE"},
        )

        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(result, "APPLICABLE")

    def test_18_evaluation_result_can_be_observation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        observation = {
            "relationship": relationship,
            "result": "APPLICABLE",
        }

        self.assertEqual(
            observation["relationship"],
            relationship,
        )
        self.assertEqual(
            observation["result"],
            "APPLICABLE",
        )

    def test_19_multiple_evaluations_can_reference_same_relationship(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        observations = [
            {
                "relationship": relationship,
                "result": "APPLICABLE",
            },
            {
                "relationship": relationship,
                "result": "NOT_APPLICABLE",
            },
        ]

        self.assertEqual(
            observations[0]["relationship"],
            observations[1]["relationship"],
        )
        self.assertNotEqual(
            observations[0]["result"],
            observations[1]["result"],
        )

    def test_20_evaluation_observation_does_not_require_relationship_mutation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        observation = {
            "relationship": relationship,
            "result": "APPLICABLE",
        }

        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(
            observation["result"],
            "APPLICABLE",
        )

    def test_21_evaluation_does_not_create_relationship_lifecycle(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result = evaluate_relationship(
            relationship,
            {"result": "APPLICABLE"},
        )

        self.assertEqual(result, "APPLICABLE")
        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )

    def test_22_relationship_and_evaluation_remain_distinct_dimensions(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result = evaluate_relationship(
            relationship,
            {"result": "APPLICABLE"},
        )

        self.assertEqual(
            relationship["source"],
            "request",
        )
        self.assertEqual(
            relationship["target"],
            "decision",
        )
        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(
            result,
            "APPLICABLE",
        )

    def test_23_final_boundary_relationship_is_not_interpretation(self):
        relationship = make_relationship(
            "request",
            "decision",
            "uses_as_input",
        )

        result = evaluate_relationship(
            relationship,
            {
                "policy": "STRICT",
                "result": "NOT_APPLICABLE",
            },
        )

        self.assertEqual(
            relationship["relation"],
            "uses_as_input",
        )
        self.assertEqual(
            result,
            "NOT_APPLICABLE",
        )


if __name__ == "__main__":
    unittest.main()