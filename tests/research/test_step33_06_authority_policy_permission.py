import unittest


class Authority:
    def __init__(self, name):
        self.name = name


class Policy:
    def __init__(self, name, conflict_behavior):
        self.name = name
        self.conflict_behavior = conflict_behavior


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class PermissionEvaluation:
    def __init__(self, authority, policy, context, permission):
        self.authority = authority
        self.policy = policy
        self.context = context
        self.permission = permission


class TestAuthorityPolicyPermission(unittest.TestCase):

    def test_authority_is_not_policy(self):
        authority = Authority("authority_a")
        policy = Policy("policy_a", "deny_on_conflict")

        self.assertNotEqual(authority, policy)

    def test_policy_is_not_permission(self):
        policy = Policy("policy_a", "deny_on_conflict")

        self.assertNotEqual(
            policy,
            ExecutionPermission.GRANTED,
        )
        self.assertNotEqual(
            policy,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_same_authority_can_be_evaluated_under_different_policies(self):
        authority = Authority("authority_a")

        policy_a = Policy("policy_a", "deny_on_conflict")
        policy_b = Policy("policy_b", "grant_on_conflict")

        evaluation_a = PermissionEvaluation(
            authority,
            policy_a,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority,
            policy_b,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            evaluation_a.authority,
            evaluation_b.authority,
        )
        self.assertNotEqual(
            evaluation_a.policy,
            evaluation_b.policy,
        )
        self.assertNotEqual(
            evaluation_a.permission,
            evaluation_b.permission,
        )

    def test_same_policy_can_evaluate_different_authorities(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        policy = Policy("policy_a", "deny_on_conflict")

        evaluation_a = PermissionEvaluation(
            authority_a,
            policy,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority_b,
            policy,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            evaluation_a.policy,
            evaluation_b.policy,
        )
        self.assertNotEqual(
            evaluation_a.authority,
            evaluation_b.authority,
        )

    def test_policy_change_does_not_create_new_authority(self):
        authority = Authority("authority_a")

        policy_a = Policy("policy_a", "deny_on_conflict")
        policy_b = Policy("policy_b", "grant_on_conflict")

        evaluation_a = PermissionEvaluation(
            authority,
            policy_a,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority,
            policy_b,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertIs(
            evaluation_a.authority,
            evaluation_b.authority,
        )

    def test_policy_change_can_change_permission(self):
        authority = Authority("authority_a")

        policy_a = Policy("policy_a", "deny_on_conflict")
        policy_b = Policy("policy_b", "grant_on_conflict")

        evaluation_a = PermissionEvaluation(
            authority,
            policy_a,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority,
            policy_b,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            evaluation_a.permission,
            evaluation_b.permission,
        )

    def test_policy_does_not_intrinsically_determine_permission(self):
        policy = Policy("policy_a", "deny_on_conflict")

        permission_a = ExecutionPermission.GRANTED
        permission_b = ExecutionPermission.NOT_GRANTED

        self.assertNotEqual(permission_a, permission_b)

        # The same Policy object can participate in evaluations
        # producing different results under different inputs.
        evaluation_a = PermissionEvaluation(
            Authority("authority_a"),
            policy,
            "context_a",
            permission_a,
        )

        evaluation_b = PermissionEvaluation(
            Authority("authority_b"),
            policy,
            "context_b",
            permission_b,
        )

        self.assertIs(
            evaluation_a.policy,
            evaluation_b.policy,
        )
        self.assertNotEqual(
            evaluation_a.permission,
            evaluation_b.permission,
        )

    def test_authority_and_policy_are_separate_inputs(self):
        authority = Authority("authority_a")
        policy = Policy("policy_a", "deny_on_conflict")

        evaluation = PermissionEvaluation(
            authority,
            policy,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertIs(
            evaluation.authority,
            authority,
        )
        self.assertIs(
            evaluation.policy,
            policy,
        )
        self.assertNotEqual(
            evaluation.authority,
            evaluation.policy,
        )

    def test_policy_can_remain_stable_while_authority_changes(self):
        policy = Policy("policy_a", "deny_on_conflict")

        evaluation_a = PermissionEvaluation(
            Authority("authority_a"),
            policy,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            Authority("authority_b"),
            policy,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertIs(
            evaluation_a.policy,
            evaluation_b.policy,
        )
        self.assertNotEqual(
            evaluation_a.authority.name,
            evaluation_b.authority.name,
        )

    def test_authority_can_remain_stable_while_policy_changes(self):
        authority = Authority("authority_a")

        evaluation_a = PermissionEvaluation(
            authority,
            Policy("policy_a", "deny_on_conflict"),
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority,
            Policy("policy_b", "grant_on_conflict"),
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertIs(
            evaluation_a.authority,
            evaluation_b.authority,
        )
        self.assertNotEqual(
            evaluation_a.policy.name,
            evaluation_b.policy.name,
        )

    def test_permission_is_evaluation_result_not_policy_identity(self):
        authority = Authority("authority_a")
        policy = Policy("policy_a", "deny_on_conflict")

        evaluation = PermissionEvaluation(
            authority,
            policy,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertNotEqual(
            evaluation.permission,
            evaluation.policy,
        )

    def test_permission_is_evaluation_result_not_authority_identity(self):
        authority = Authority("authority_a")
        policy = Policy("policy_a", "deny_on_conflict")

        evaluation = PermissionEvaluation(
            authority,
            policy,
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertNotEqual(
            evaluation.permission,
            evaluation.authority,
        )

    def test_policy_is_not_execution_occurrence(self):
        policy = Policy("policy_a", "deny_on_conflict")

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertIsNotNone(policy)

    def test_policy_change_does_not_require_execution(self):
        authority = Authority("authority_a")

        evaluation_a = PermissionEvaluation(
            authority,
            Policy("policy_a", "deny_on_conflict"),
            "context_a",
            ExecutionPermission.NOT_GRANTED,
        )

        evaluation_b = PermissionEvaluation(
            authority,
            Policy("policy_b", "grant_on_conflict"),
            "context_a",
            ExecutionPermission.GRANTED,
        )

        execution_id = None

        self.assertNotEqual(
            evaluation_a.policy.name,
            evaluation_b.policy.name,
        )
        self.assertIsNone(execution_id)

    def test_policy_is_a_possible_input_to_permission_evaluation(self):
        authority = Authority("authority_a")
        policy = Policy("policy_a", "deny_on_conflict")

        evaluation = PermissionEvaluation(
            authority,
            policy,
            "context_a",
            ExecutionPermission.GRANTED,
        )

        self.assertIsNotNone(evaluation.policy)
        self.assertIsNotNone(evaluation.permission)


if __name__ == "__main__":
    unittest.main()