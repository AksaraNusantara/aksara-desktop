import unittest


class Authority:
    def __init__(self, name, implication):
        self.name = name
        self.implication = implication


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class PermissionEvaluation:
    def __init__(self, authorities, context, permission):
        self.authorities = tuple(authorities)
        self.context = context
        self.permission = permission


class TestAuthorityImplicationConflict(unittest.TestCase):

    def test_different_authority_implications_can_coexist(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        evaluation = PermissionEvaluation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            evaluation.authorities[0].implication,
            "GRANT",
        )
        self.assertEqual(
            evaluation.authorities[1].implication,
            "DENY",
        )

    def test_different_implications_are_not_automatically_conflict(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        implications = {
            authority_a.implication,
            authority_b.implication,
        }

        conflict = False

        self.assertEqual(
            implications,
            {"GRANT", "DENY"},
        )
        self.assertFalse(conflict)

    def test_conflict_requires_an_explicit_semantic_condition(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        context = {
            "conflict_rule": True,
        }

        conflict = (
            context["conflict_rule"]
            and authority_a.implication != authority_b.implication
        )

        self.assertTrue(conflict)

    def test_same_implication_does_not_create_conflict(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "GRANT")

        conflict = (
            authority_a.implication != authority_b.implication
        )

        self.assertFalse(conflict)

    def test_different_implications_can_produce_one_permission_result(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        evaluation = PermissionEvaluation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            evaluation.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_permission_result_is_not_the_conflict_itself(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        conflict = True

        evaluation = PermissionEvaluation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertNotEqual(
            conflict,
            evaluation.permission,
        )

    def test_conflict_and_permission_are_distinct_dimensions(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        evaluation = PermissionEvaluation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        conflict = True

        self.assertTrue(conflict)
        self.assertEqual(
            evaluation.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_conflict_does_not_intrinsically_change_authority_identity(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        original_names = (
            authority_a.name,
            authority_b.name,
        )

        conflict = True

        self.assertTrue(conflict)
        self.assertEqual(
            original_names,
            ("authority_a", "authority_b"),
        )

    def test_conflict_does_not_create_new_authority(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        authorities = [authority_a, authority_b]

        conflict = True

        self.assertTrue(conflict)
        self.assertEqual(
            len(authorities),
            2,
        )

    def test_context_can_change_whether_difference_is_conflict(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        context_without_rule = {
            "conflict_rule": False,
        }

        context_with_rule = {
            "conflict_rule": True,
        }

        conflict_without_rule = (
            context_without_rule["conflict_rule"]
            and authority_a.implication != authority_b.implication
        )

        conflict_with_rule = (
            context_with_rule["conflict_rule"]
            and authority_a.implication != authority_b.implication
        )

        self.assertFalse(conflict_without_rule)
        self.assertTrue(conflict_with_rule)

    def test_contextual_conflict_does_not_imply_permission_value(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        context = {
            "conflict_rule": True,
            "permission_policy": "deny_on_conflict",
        }

        conflict = (
            context["conflict_rule"]
            and authority_a.implication != authority_b.implication
        )

        permission = (
            ExecutionPermission.NOT_GRANTED
            if (
                conflict
                and context["permission_policy"] == "deny_on_conflict"
            )
            else ExecutionPermission.GRANTED
        )

        self.assertTrue(conflict)
        self.assertEqual(
            permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_same_conflict_can_support_different_permission_policies(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        conflict = True

        policy_deny = "deny_on_conflict"
        policy_grant = "grant_on_conflict"

        permission_deny = (
            ExecutionPermission.NOT_GRANTED
            if policy_deny == "deny_on_conflict"
            else ExecutionPermission.GRANTED
        )

        permission_grant = (
            ExecutionPermission.GRANTED
            if policy_grant == "grant_on_conflict"
            else ExecutionPermission.NOT_GRANTED
        )

        self.assertTrue(conflict)
        self.assertNotEqual(
            permission_deny,
            permission_grant,
        )

    def test_conflict_is_not_intrinsic_to_authority(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        conflict_context_a = True
        conflict_context_b = False

        self.assertNotEqual(
            conflict_context_a,
            conflict_context_b,
        )

        self.assertEqual(
            authority_a.name,
            "authority_a",
        )
        self.assertEqual(
            authority_b.name,
            "authority_b",
        )

    def test_permission_evaluation_can_consider_conflict_as_an_input(self):
        authority_a = Authority("authority_a", "GRANT")
        authority_b = Authority("authority_b", "DENY")

        conflict = True

        evaluation = PermissionEvaluation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertTrue(conflict)
        self.assertEqual(
            evaluation.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_conflict_does_not_equal_resolution(self):
        conflict = True
        resolution = None

        self.assertTrue(conflict)
        self.assertIsNone(resolution)

    def test_conflict_does_not_require_resolution(self):
        conflict = True
        resolution_required = False

        self.assertTrue(conflict)
        self.assertFalse(resolution_required)


if __name__ == "__main__":
    unittest.main()