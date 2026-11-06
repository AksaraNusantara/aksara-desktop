import unittest


def evaluate_applicability(scope, resolution, policy):
    if not policy["enabled"]:
        return False

    return resolution["allowed_scope"] == scope


class TestAdmissionDecisionOrderingAuthorityConflictResolutionApplicabilityStability(
    unittest.TestCase
):

    def test_same_inputs_produce_same_result(self):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        first = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        second = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        self.assertEqual(first, second)
        self.assertTrue(first)

    def test_repeated_evaluation_does_not_change_result(self):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        results = [
            evaluate_applicability(
                scope,
                resolution,
                policy,
            )
            for _ in range(5)
        ]

        self.assertEqual(
            results,
            [True, True, True, True, True],
        )

    def test_representation_change_does_not_change_result(self):
        scope_list = ["scope-a"]
        scope_string = "scope-a"

        resolution_a = {
            "allowed_scope": "scope-a",
        }

        resolution_b = dict(resolution_a)

        policy_a = {
            "enabled": True,
        }

        policy_b = dict(policy_a)

        result_a = evaluate_applicability(
            scope_list[0],
            resolution_a,
            policy_a,
        )

        result_b = evaluate_applicability(
            scope_string,
            resolution_b,
            policy_b,
        )

        self.assertEqual(result_a, result_b)
        self.assertTrue(result_a)

    def test_scope_change_can_change_result(self):
        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        result_a = evaluate_applicability(
            "scope-a",
            resolution,
            policy,
        )

        result_b = evaluate_applicability(
            "scope-b",
            resolution,
            policy,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

    def test_resolution_change_can_change_result(self):
        scope = "scope-a"

        resolution_a = {
            "allowed_scope": "scope-a",
        }

        resolution_b = {
            "allowed_scope": "scope-b",
        }

        policy = {
            "enabled": True,
        }

        result_a = evaluate_applicability(
            scope,
            resolution_a,
            policy,
        )

        result_b = evaluate_applicability(
            scope,
            resolution_b,
            policy,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

    def test_policy_change_can_change_result(self):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        enabled_policy = {
            "enabled": True,
        }

        disabled_policy = {
            "enabled": False,
        }

        result_enabled = evaluate_applicability(
            scope,
            resolution,
            enabled_policy,
        )

        result_disabled = evaluate_applicability(
            scope,
            resolution,
            disabled_policy,
        )

        self.assertTrue(result_enabled)
        self.assertFalse(result_disabled)

    def test_scope_object_can_remain_unchanged_across_evaluations(
        self,
    ):
        scope = {
            "scope_id": "scope-a",
        }

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        before = dict(scope)

        evaluate_applicability(
            scope["scope_id"],
            resolution,
            policy,
        )

        self.assertEqual(scope, before)

    def test_resolution_object_can_remain_unchanged_across_evaluations(
        self,
    ):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        before = dict(resolution)

        evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        self.assertEqual(resolution, before)

    def test_policy_object_can_remain_unchanged_across_evaluations(
        self,
    ):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        before = dict(policy)

        evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        self.assertEqual(policy, before)

    def test_same_semantic_inputs_have_stable_result_after_copying(
        self,
    ):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        copied_resolution = dict(resolution)
        copied_policy = dict(policy)

        result_original = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        result_copied = evaluate_applicability(
            scope,
            copied_resolution,
            copied_policy,
        )

        self.assertEqual(
            result_original,
            result_copied,
        )

    def test_policy_is_a_semantic_input_when_it_controls_applicability(
        self,
    ):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": False,
        }

        result = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        self.assertFalse(result)

    def test_stability_does_not_require_applicability_identity(
        self,
    ):
        scope = "scope-a"

        resolution = {
            "allowed_scope": "scope-a",
        }

        policy = {
            "enabled": True,
        }

        first = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        second = evaluate_applicability(
            scope,
            resolution,
            policy,
        )

        self.assertEqual(first, second)

        observation_a = {
            "applicable": first,
        }

        observation_b = {
            "applicable": second,
        }

        self.assertEqual(
            observation_a,
            observation_b,
        )


if __name__ == "__main__":
    unittest.main()