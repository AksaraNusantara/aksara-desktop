import unittest


def resolve_by_scope(
    scope,
    authority_a,
    authority_b,
    policy,
):
    if policy == "prefer-authority-a":
        return authority_a

    if policy == "prefer-authority-b":
        return authority_b

    if policy == "prefer-by-scope":
        if scope == "scope-a":
            return authority_a

        if scope == "scope-b":
            return authority_b

    return None


class TestAdmissionDecisionOrderingAuthorityConflictResolutionScopeSemantics(
    unittest.TestCase
):

    def test_same_scope_same_policy_same_outcome(self):
        first = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        second = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        self.assertEqual(first, second)

    def test_different_scope_can_change_outcome(self):
        outcome_a = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        outcome_b = resolve_by_scope(
            scope="scope-b",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        self.assertNotEqual(outcome_a, outcome_b)

    def test_scope_can_be_semantically_relevant(self):
        outcome = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        self.assertEqual(
            outcome,
            "authority-a",
        )

    def test_scope_does_not_override_explicit_policy(self):
        outcome_a = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        outcome_b = resolve_by_scope(
            scope="scope-b",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertEqual(outcome_a, "authority-b")
        self.assertEqual(outcome_b, "authority-b")

    def test_policy_can_decide_whether_scope_matters(self):
        scoped = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        explicit = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-authority-b",
        )

        self.assertNotEqual(scoped, explicit)

    def test_same_authorities_can_have_different_scope_semantics(self):
        outcome_a = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        outcome_b = resolve_by_scope(
            scope="scope-b",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        self.assertEqual(outcome_a, "authority-a")
        self.assertEqual(outcome_b, "authority-b")

    def test_scope_change_does_not_mutate_authority_identity(self):
        authority_a = "authority-a"
        authority_b = "authority-b"

        first = resolve_by_scope(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
            policy="prefer-by-scope",
        )

        second = resolve_by_scope(
            scope="scope-b",
            authority_a=authority_a,
            authority_b=authority_b,
            policy="prefer-by-scope",
        )

        self.assertEqual(authority_a, "authority-a")
        self.assertEqual(authority_b, "authority-b")
        self.assertNotEqual(first, second)

    def test_scope_change_does_not_require_new_authority(self):
        outcome_a = resolve_by_scope(
            scope="scope-a",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        outcome_b = resolve_by_scope(
            scope="scope-b",
            authority_a="authority-a",
            authority_b="authority-b",
            policy="prefer-by-scope",
        )

        self.assertIn(
            outcome_a,
            {"authority-a", "authority-b"},
        )

        self.assertIn(
            outcome_b,
            {"authority-a", "authority-b"},
        )

    def test_scope_semantics_can_exist_without_scope_object(self):
        context = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "policy": "prefer-by-scope",
        }

        outcome = resolve_by_scope(
            scope=context["scope"],
            authority_a=context["authority_a"],
            authority_b=context["authority_b"],
            policy=context["policy"],
        )

        self.assertEqual(
            outcome,
            "authority-a",
        )

    def test_scope_is_context_not_resolution_identity(self):
        context = {
            "scope": "scope-a",
            "resolution": {
                "selected_authority": "authority-a"
            },
        }

        self.assertEqual(
            context["scope"],
            "scope-a",
        )

        self.assertEqual(
            context["resolution"]["selected_authority"],
            "authority-a",
        )

        self.assertNotEqual(
            context["scope"],
            context["resolution"]["selected_authority"],
        )

    def test_resolution_can_be_same_type_across_scopes(self):
        resolution_a = {
            "selected_authority": "authority-a"
        }

        resolution_b = {
            "selected_authority": "authority-b"
        }

        self.assertEqual(
            set(resolution_a.keys()),
            set(resolution_b.keys()),
        )

    def test_minimal_model_can_use_scope_as_external_input(self):
        scope = "scope-a"
        authority_a = "authority-a"
        authority_b = "authority-b"
        policy = "prefer-by-scope"

        outcome = resolve_by_scope(
            scope,
            authority_a,
            authority_b,
            policy,
        )

        self.assertEqual(
            outcome,
            "authority-a",
        )


if __name__ == "__main__":
    unittest.main()