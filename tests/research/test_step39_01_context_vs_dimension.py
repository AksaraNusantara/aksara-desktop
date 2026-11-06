import unittest


def make_context(name, purpose):
    return {
        "name": name,
        "purpose": purpose,
    }


def make_dimension(name, value):
    return {
        "name": name,
        "value": value,
    }


def evaluate_in_context(context, dimension):
    return {
        "context": context,
        "dimension": dimension,
    }


class TestContextVsDimension(unittest.TestCase):

    def test_01_context_can_coexist_with_identity(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        identity = make_dimension(
            "identity",
            "REQ-001",
        )

        observation = evaluate_in_context(
            context,
            identity,
        )

        self.assertEqual(
            observation["context"]["name"],
            "execution_context",
        )
        self.assertEqual(
            observation["dimension"]["name"],
            "identity",
        )

    def test_02_context_can_coexist_with_state(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        state = make_dimension(
            "state",
            "ACTIVE",
        )

        observation = evaluate_in_context(
            context,
            state,
        )

        self.assertEqual(
            observation["dimension"]["value"],
            "ACTIVE",
        )

    def test_03_context_can_coexist_with_ordering(self):
        context = make_context(
            "ordering_context",
            "ordering_interpretation",
        )

        ordering = make_dimension(
            "ordering",
            "FIRST",
        )

        observation = evaluate_in_context(
            context,
            ordering,
        )

        self.assertEqual(
            observation["context"]["name"],
            "ordering_context",
        )
        self.assertEqual(
            observation["dimension"]["name"],
            "ordering",
        )

    def test_04_context_can_coexist_with_constraint(self):
        context = make_context(
            "validation_context",
            "constraint_evaluation",
        )

        constraint = make_dimension(
            "constraint",
            "identity_required",
        )

        observation = evaluate_in_context(
            context,
            constraint,
        )

        self.assertEqual(
            observation["dimension"]["value"],
            "identity_required",
        )

    def test_05_context_can_coexist_with_relationship(self):
        context = make_context(
            "relationship_context",
            "relationship_interpretation",
        )

        relationship = make_dimension(
            "relationship",
            "A_REQUIRES_B",
        )

        observation = evaluate_in_context(
            context,
            relationship,
        )

        self.assertEqual(
            observation["dimension"]["value"],
            "A_REQUIRES_B",
        )

    def test_06_context_can_coexist_with_constraint_result(self):
        context = make_context(
            "constraint_context",
            "constraint_evaluation",
        )

        result = make_dimension(
            "constraint_result",
            "SATISFIED",
        )

        observation = evaluate_in_context(
            context,
            result,
        )

        self.assertEqual(
            observation["dimension"]["value"],
            "SATISFIED",
        )

    def test_07_context_is_not_identity(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        identity = "REQ-001"

        self.assertNotEqual(
            context["name"],
            identity,
        )

    def test_08_context_is_not_state(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        states = {
            "ACTIVE",
            "INACTIVE",
        }

        self.assertNotIn(
            context["name"],
            states,
        )

    def test_09_context_is_not_ordering(self):
        context = make_context(
            "ordering_context",
            "ordering_interpretation",
        )

        orderings = {
            "FIRST",
            "SECOND",
            "BEFORE",
            "AFTER",
        }

        self.assertNotIn(
            context["name"],
            orderings,
        )

    def test_10_context_is_not_constraint(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        constraints = {
            "identity_required",
            "state_required",
        }

        self.assertNotIn(
            context["name"],
            constraints,
        )

    def test_11_context_is_not_constraint_result(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        results = {
            "SATISFIED",
            "VIOLATED",
        }

        self.assertNotIn(
            context["name"],
            results,
        )

    def test_12_context_is_not_relationship(self):
        context = make_context(
            "relationship_context",
            "relationship_interpretation",
        )

        relationship = (
            "A",
            "REQUIRES",
            "B",
        )

        self.assertNotEqual(
            context["name"],
            relationship,
        )

    def test_13_context_can_reference_multiple_dimensions(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimensions = [
            make_dimension("identity", "REQ-001"),
            make_dimension("state", "ACTIVE"),
            make_dimension("ordering", "FIRST"),
        ]

        observations = [
            evaluate_in_context(context, dimension)
            for dimension in dimensions
        ]

        self.assertEqual(
            len(observations),
            3,
        )

    def test_14_multiple_contexts_can_reference_same_dimension(self):
        identity = make_dimension(
            "identity",
            "REQ-001",
        )

        context_a = make_context(
            "context_a",
            "purpose_a",
        )

        context_b = make_context(
            "context_b",
            "purpose_b",
        )

        observation_a = evaluate_in_context(
            context_a,
            identity,
        )

        observation_b = evaluate_in_context(
            context_b,
            identity,
        )

        self.assertEqual(
            observation_a["dimension"],
            observation_b["dimension"],
        )

    def test_15_same_context_can_reference_multiple_dimensions(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimensions = [
            make_dimension("identity", "REQ-001"),
            make_dimension("state", "ACTIVE"),
            make_dimension("constraint", "identity_required"),
        ]

        observations = [
            evaluate_in_context(context, dimension)
            for dimension in dimensions
        ]

        self.assertEqual(
            len(observations),
            3,
        )

    def test_16_context_does_not_become_composite_dimension(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimensions = [
            make_dimension("identity", "REQ-001"),
            make_dimension("state", "ACTIVE"),
        ]

        observation = evaluate_in_context(
            context,
            dimensions,
        )

        self.assertIs(
            observation["context"],
            context,
        )
        self.assertEqual(
            observation["dimension"],
            dimensions,
        )

    def test_17_context_identity_is_distinct_from_dimension_identity(self):
        context_id = "CTX-001"
        dimension_id = "REQ-001"

        self.assertNotEqual(
            context_id,
            dimension_id,
        )

    def test_18_context_can_exist_without_identity_dimension(self):
        context = make_context(
            "policy_context",
            "policy_interpretation",
        )

        self.assertIsNotNone(context)

    def test_19_context_can_exist_without_state_dimension(self):
        context = make_context(
            "policy_context",
            "policy_interpretation",
        )

        self.assertIsNotNone(context)

    def test_20_context_can_exist_without_constraint(self):
        context = make_context(
            "observation_context",
            "observation_interpretation",
        )

        self.assertIsNotNone(context)

    def test_21_context_does_not_require_evaluation_result(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        self.assertNotIn(
            "result",
            context,
        )

    def test_22_context_can_be_used_as_evaluation_frame(self):
        context = make_context(
            "constraint_context",
            "constraint_evaluation",
        )

        constraint = make_dimension(
            "constraint",
            "identity_required",
        )

        observation = evaluate_in_context(
            context,
            constraint,
        )

        self.assertEqual(
            observation["context"]["purpose"],
            "constraint_evaluation",
        )

    def test_23_context_does_not_change_dimension_identity(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimension = make_dimension(
            "identity",
            "REQ-001",
        )

        before = dimension["name"]

        evaluate_in_context(
            context,
            dimension,
        )

        after = dimension["name"]

        self.assertEqual(
            before,
            after,
        )

    def test_24_context_does_not_change_dimension_value(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimension = make_dimension(
            "state",
            "ACTIVE",
        )

        before = dimension["value"]

        evaluate_in_context(
            context,
            dimension,
        )

        after = dimension["value"]

        self.assertEqual(
            before,
            after,
        )

    def test_25_context_is_distinct_from_dimension(self):
        context = make_context(
            "execution_context",
            "execution_interpretation",
        )

        dimension = make_dimension(
            "state",
            "ACTIVE",
        )

        self.assertIsNot(
            context,
            dimension,
        )


if __name__ == "__main__":
    unittest.main()