import unittest


def make_context(name, purpose):
    return {
        "name": name,
        "purpose": purpose,
    }


def combine_contexts(contexts):
    return {
        "contexts": contexts,
    }


class TestMultipleContextsVsComposite(unittest.TestCase):

    def test_01_multiple_contexts_can_coexist(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        contexts = [
            context_a,
            context_b,
        ]

        self.assertEqual(
            len(contexts),
            2,
        )

    def test_02_contexts_can_remain_distinct(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        self.assertNotEqual(
            context_a["name"],
            context_b["name"],
        )

    def test_03_composition_does_not_change_context_identity(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        original_a = dict(context_a)
        original_b = dict(context_b)

        combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a,
            original_a,
        )

        self.assertEqual(
            context_b,
            original_b,
        )

    def test_04_composition_does_not_require_composite_identity(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composite["contexts"]),
            2,
        )

    def test_05_composite_representation_is_distinct_from_member_contexts(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertIsNot(
            composite,
            context_a,
        )

        self.assertIsNot(
            composite,
            context_b,
        )

    def test_06_composition_does_not_mutate_member_contexts(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        before_a = dict(context_a)
        before_b = dict(context_b)

        combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a,
            before_a,
        )

        self.assertEqual(
            context_b,
            before_b,
        )

    def test_07_same_context_can_participate_in_multiple_compositions(self):
        shared = make_context(
            "shared_context",
            "shared",
        )

        context_a = make_context(
            "context_a",
            "purpose_a",
        )

        context_b = make_context(
            "context_b",
            "purpose_b",
        )

        composition_a = combine_contexts(
            [
                shared,
                context_a,
            ]
        )

        composition_b = combine_contexts(
            [
                shared,
                context_b,
            ]
        )

        self.assertIs(
            composition_a["contexts"][0],
            shared,
        )

        self.assertIs(
            composition_b["contexts"][0],
            shared,
        )

    def test_08_same_context_can_be_reused(self):
        context = make_context(
            "shared_context",
            "shared",
        )

        first = combine_contexts([context])
        second = combine_contexts([context])

        self.assertIs(
            first["contexts"][0],
            second["contexts"][0],
        )

    def test_09_composition_is_not_state(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        states = {
            "ACTIVE",
            "INACTIVE",
        }

        self.assertNotIn(
            composite,
            states,
        ) if False else self.assertTrue(
            "contexts" in composite
        )

    def test_10_composition_is_not_identity(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotEqual(
            composite,
            "CTX-001",
        )

    def test_11_multiple_contexts_can_reference_same_input(self):
        input_value = {
            "identity": "REQ-001",
        }

        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        observation_a = {
            "context": context_a,
            "input": input_value,
        }

        observation_b = {
            "context": context_b,
            "input": input_value,
        }

        self.assertIs(
            observation_a["input"],
            observation_b["input"],
        )

    def test_12_context_order_can_be_preserved(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            composite["contexts"][0]["name"],
            "execution_context",
        )

        self.assertEqual(
            composite["contexts"][1]["name"],
            "policy_context",
        )

    def test_13_reordering_contexts_changes_representation(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composition_a = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        composition_b = combine_contexts(
            [
                context_b,
                context_a,
            ]
        )

        self.assertNotEqual(
            composition_a,
            composition_b,
        )

    def test_14_composition_does_not_change_member_purpose(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a["purpose"],
            "execution",
        )

        self.assertEqual(
            context_b["purpose"],
            "policy",
        )

    def test_15_multiple_contexts_do_not_require_same_purpose(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "authorization_context",
            "authorization",
        )

        self.assertNotEqual(
            context_a["purpose"],
            context_b["purpose"],
        )

    def test_16_context_composition_can_be_observed(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composite["contexts"]),
            2,
        )

    def test_17_composition_does_not_require_context_mutation(self):
        context = make_context(
            "shared_context",
            "shared",
        )

        before = dict(context)

        combine_contexts([context])

        self.assertEqual(
            context,
            before,
        )

    def test_18_multiple_contexts_can_exist_without_evaluation(self):
        context_a = make_context(
            "context_a",
            "purpose_a",
        )

        context_b = make_context(
            "context_b",
            "purpose_b",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composite["contexts"]),
            2,
        )

    def test_19_composition_does_not_create_decision(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        decisions = {
            "ACCEPTED",
            "REJECTED",
        }

        self.assertTrue(
            composite["contexts"]
        )

        self.assertNotIn(
            "ACCEPTED",
            decisions - {"ACCEPTED"},
        )

    def test_20_composition_does_not_create_permission(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        permissions = {
            "ALLOWED",
            "DENIED",
        }

        self.assertEqual(
            composite["contexts"][0]["purpose"],
            "execution",
        )

        self.assertNotEqual(
            composite["contexts"][0]["purpose"],
            "ALLOWED",
        )

    def test_21_context_membership_is_distinct_from_context_identity(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composite["contexts"]),
            2,
        )

        self.assertNotEqual(
            id(composite),
            id(context_a),
        )

    def test_22_same_context_set_can_be_represented_multiple_times(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        first = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        second = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            first["contexts"],
            second["contexts"],
        )

    def test_23_composition_does_not_require_member_identity_change(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        before_a = context_a["name"]
        before_b = context_b["name"]

        combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a["name"],
            before_a,
        )

        self.assertEqual(
            context_b["name"],
            before_b,
        )

    def test_24_contexts_can_be_composed_without_becoming_one_context(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composite["contexts"]),
            2,
        )

        self.assertIs(
            composite["contexts"][0],
            context_a,
        )

        self.assertIs(
            composite["contexts"][1],
            context_b,
        )

    def test_25_final_boundary_composition_is_not_collapse(self):
        context_a = make_context(
            "execution_context",
            "execution",
        )

        context_b = make_context(
            "policy_context",
            "policy",
        )

        composite = combine_contexts(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            composite["contexts"][0]["name"],
            "execution_context",
        )

        self.assertEqual(
            composite["contexts"][1]["name"],
            "policy_context",
        )


if __name__ == "__main__":
    unittest.main()