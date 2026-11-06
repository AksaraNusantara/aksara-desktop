import unittest


def make_context(context_id, name):
    return {
        "id": context_id,
        "name": name,
    }


def compose(contexts):
    return {
        "contexts": contexts,
    }


class TestContextCompositionIdentity(unittest.TestCase):

    def test_01_each_context_has_distinct_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        self.assertNotEqual(
            context_a["id"],
            context_b["id"],
        )

    def test_02_composition_preserves_member_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            composition["contexts"][0]["id"],
            "CTX-A",
        )

        self.assertEqual(
            composition["contexts"][1]["id"],
            "CTX-B",
        )

    def test_03_composition_does_not_mutate_context_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a["id"],
            "CTX-A",
        )

        self.assertEqual(
            context_b["id"],
            "CTX-B",
        )

    def test_04_composition_identity_is_not_required(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotIn(
            "id",
            composition,
        )

    def test_05_member_identity_is_not_composite_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotEqual(
            composition["contexts"][0]["id"],
            composition["contexts"][1]["id"],
        )

    def test_06_same_context_identity_can_participate_in_multiple_compositions(self):
        shared = make_context(
            "CTX-SHARED",
            "shared",
        )

        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition_a = compose(
            [
                shared,
                context_a,
            ]
        )

        composition_b = compose(
            [
                shared,
                context_b,
            ]
        )

        self.assertEqual(
            composition_a["contexts"][0]["id"],
            "CTX-SHARED",
        )

        self.assertEqual(
            composition_b["contexts"][0]["id"],
            "CTX-SHARED",
        )

    def test_07_composition_does_not_require_new_member_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        before_a = context_a["id"]
        before_b = context_b["id"]

        compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            context_a["id"],
            before_a,
        )

        self.assertEqual(
            context_b["id"],
            before_b,
        )

    def test_08_context_identity_remains_stable_across_compositions(self):
        context = make_context(
            "CTX-A",
            "execution",
        )

        first = compose([context])
        second = compose([context])

        self.assertEqual(
            first["contexts"][0]["id"],
            second["contexts"][0]["id"],
        )

    def test_09_different_compositions_can_reference_same_context(self):
        context = make_context(
            "CTX-A",
            "execution",
        )

        other_a = make_context(
            "CTX-B",
            "policy",
        )

        other_b = make_context(
            "CTX-C",
            "authorization",
        )

        first = compose(
            [
                context,
                other_a,
            ]
        )

        second = compose(
            [
                context,
                other_b,
            ]
        )

        self.assertEqual(
            first["contexts"][0]["id"],
            "CTX-A",
        )

        self.assertEqual(
            second["contexts"][0]["id"],
            "CTX-A",
        )

    def test_10_context_identity_is_distinct_from_composition_membership(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            len(composition["contexts"]),
            2,
        )

        self.assertNotEqual(
            context_a["id"],
            "COMPOSITION",
        )

    def test_11_composition_does_not_create_context_state(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotIn(
            "state",
            composition,
        )

    def test_12_composition_does_not_create_lifecycle(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotIn(
            "lifecycle",
            composition,
        )

    def test_13_context_identity_does_not_depend_on_composition(self):
        context = make_context(
            "CTX-A",
            "execution",
        )

        original_identity = context["id"]

        compose([context])

        self.assertEqual(
            context["id"],
            original_identity,
        )

    def test_14_context_identity_can_exist_without_composition(self):
        context = make_context(
            "CTX-A",
            "execution",
        )

        self.assertEqual(
            context["id"],
            "CTX-A",
        )

    def test_15_composition_can_exist_without_new_context_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        identities = [
            context["id"]
            for context in composition["contexts"]
        ]

        self.assertEqual(
            identities,
            [
                "CTX-A",
                "CTX-B",
            ],
        )

    def test_16_same_member_identities_can_appear_in_multiple_observations(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        first = compose(
            [
                context_a,
                context_b,
            ]
        )

        second = compose(
            [
                context_a,
                context_b,
            ]
        )

        first_ids = [
            context["id"]
            for context in first["contexts"]
        ]

        second_ids = [
            context["id"]
            for context in second["contexts"]
        ]

        self.assertEqual(
            first_ids,
            second_ids,
        )

    def test_17_context_identity_is_not_composition_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotEqual(
            context_a["id"],
            "COMPOSITE-1",
        )

        self.assertNotEqual(
            context_b["id"],
            "COMPOSITE-1",
        )

        self.assertIsNotNone(
            composition,
        )

    def test_18_composition_does_not_require_context_identity_fusion(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        ids = {
            context["id"]
            for context in composition["contexts"]
        }

        self.assertEqual(
            ids,
            {
                "CTX-A",
                "CTX-B",
            },
        )

    def test_19_context_identity_survives_reordering(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        first = compose(
            [
                context_a,
                context_b,
            ]
        )

        second = compose(
            [
                context_b,
                context_a,
            ]
        )

        first_ids = {
            context["id"]
            for context in first["contexts"]
        }

        second_ids = {
            context["id"]
            for context in second["contexts"]
        }

        self.assertEqual(
            first_ids,
            second_ids,
        )

    def test_20_reordering_does_not_change_member_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        compose(
            [
                context_b,
                context_a,
            ]
        )

        self.assertEqual(
            context_a["id"],
            "CTX-A",
        )

        self.assertEqual(
            context_b["id"],
            "CTX-B",
        )

    def test_21_context_identity_is_not_context_purpose(self):
        context = make_context(
            "CTX-A",
            "execution",
        )

        self.assertNotEqual(
            context["id"],
            context["name"],
        )

    def test_22_multiple_contexts_can_have_independent_identity(self):
        contexts = [
            make_context(
                "CTX-A",
                "execution",
            ),
            make_context(
                "CTX-B",
                "policy",
            ),
            make_context(
                "CTX-C",
                "authorization",
            ),
        ]

        identities = [
            context["id"]
            for context in contexts
        ]

        self.assertEqual(
            identities,
            [
                "CTX-A",
                "CTX-B",
                "CTX-C",
            ],
        )

    def test_23_composition_preserves_all_member_identities(self):
        contexts = [
            make_context(
                "CTX-A",
                "execution",
            ),
            make_context(
                "CTX-B",
                "policy",
            ),
            make_context(
                "CTX-C",
                "authorization",
            ),
        ]

        composition = compose(contexts)

        identities = [
            context["id"]
            for context in composition["contexts"]
        ]

        self.assertEqual(
            identities,
            [
                "CTX-A",
                "CTX-B",
                "CTX-C",
            ],
        )

    def test_24_composition_is_not_identity_substitute(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertNotEqual(
            composition,
            context_a["id"],
        )

        self.assertNotEqual(
            composition,
            context_b["id"],
        )

    def test_25_final_boundary_composition_does_not_require_new_context_identity(self):
        context_a = make_context(
            "CTX-A",
            "execution",
        )

        context_b = make_context(
            "CTX-B",
            "policy",
        )

        composition = compose(
            [
                context_a,
                context_b,
            ]
        )

        self.assertEqual(
            composition["contexts"][0]["id"],
            "CTX-A",
        )

        self.assertEqual(
            composition["contexts"][1]["id"],
            "CTX-B",
        )


if __name__ == "__main__":
    unittest.main()