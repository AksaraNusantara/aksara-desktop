import unittest


def resolve_minimal(
    scope,
    authority_a,
    authority_b,
    policy,
):
    if policy == "prefer-authority-a":
        return authority_a

    if policy == "prefer-authority-b":
        return authority_b

    return None


class TestAdmissionDecisionOrderingAuthorityConflictMinimalResolution(
    unittest.TestCase
):

    def test_scope_is_sufficient_context(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(result, "authority-a")

    def test_competing_authorities_are_sufficient(self):
        result_a = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        result_b = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertNotEqual(result_a, result_b)

    def test_resolution_object_is_not_required(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(result, "authority-a")

    def test_conflict_object_is_not_required(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertEqual(result, "authority-b")

    def test_resolution_id_is_not_required(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertIsNotNone(result)

    def test_resolution_authority_is_not_required(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(result, "authority-a")

    def test_observation_is_not_required_for_resolution(self):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(result, "authority-a")

    def test_request_identity_is_not_required_for_minimal_resolution(
        self,
    ):
        result = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(result, "authority-a")

    def test_policy_is_semantically_relevant(self):
        result_a = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        result_b = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertNotEqual(result_a, result_b)

    def test_same_inputs_produce_stable_outcome(self):
        first = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        second = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        self.assertEqual(first, second)

    def test_different_scope_can_have_independent_resolution(self):
        result_a = resolve_minimal(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-a",
        )

        result_b = resolve_minimal(
            scope="scope-b",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertEqual(result_a, "authority-a")
        self.assertEqual(result_b, "authority-b")

    def test_minimal_model_preserves_resolution_boundary(self):
        context = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "policy": "prefer-authority-a",
        }

        outcome = resolve_minimal(
            scope=context["scope"],
            authority_a=context["authority_a"],
            authority_b=context["authority_b"],
            policy=context["policy"],
        )

        self.assertEqual(
            outcome,
            "authority-a",
        )


if __name__ == "__main__":
    unittest.main()