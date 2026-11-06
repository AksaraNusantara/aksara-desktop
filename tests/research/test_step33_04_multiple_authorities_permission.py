import unittest


class Authority:
    def __init__(self, name):
        self.name = name


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class PermissionObservation:
    def __init__(self, authorities, context, permission):
        self.authorities = tuple(authorities)
        self.context = context
        self.permission = permission


class TestMultipleAuthoritiesPermission(unittest.TestCase):

    def test_multiple_authorities_can_be_observed_together(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.authorities,
            (authority_a, authority_b),
        )

    def test_permission_is_not_identical_to_authority_set(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation.authorities,
            observation.permission,
        )

    def test_same_authority_set_can_have_different_permissions(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        granted = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        not_granted = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_b",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(granted.authorities, not_granted.authorities)
        self.assertNotEqual(granted.permission, not_granted.permission)

    def test_context_can_change_permission_for_same_authority_set(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation_a = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_b = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_b",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation_a.authorities,
            observation_b.authorities,
        )
        self.assertNotEqual(
            observation_a.context,
            observation_b.context,
        )
        self.assertNotEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_changing_one_authority_can_change_permission(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")
        authority_c = Authority("authority_c")

        observation_a = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_b = PermissionObservation(
            authorities=[authority_a, authority_c],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertNotEqual(
            observation_a.authorities,
            observation_b.authorities,
        )
        self.assertNotEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_authority_set_does_not_intrinsically_contain_permission(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        authorities = (authority_a, authority_b)

        self.assertFalse(
            hasattr(authorities, "permission")
        )

    def test_same_authority_can_participate_in_different_authority_sets(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")
        authority_c = Authority("authority_c")

        observation_a = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_b = PermissionObservation(
            authorities=[authority_a, authority_c],
            context="context_a",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertIn(authority_a, observation_a.authorities)
        self.assertIn(authority_a, observation_b.authorities)

    def test_permission_is_not_intrinsic_to_individual_authority(self):
        authority_a = Authority("authority_a")

        observation_granted = PermissionObservation(
            authorities=[authority_a],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_not_granted = PermissionObservation(
            authorities=[authority_a],
            context="context_b",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation_granted.authorities,
            observation_not_granted.authorities,
        )
        self.assertNotEqual(
            observation_granted.permission,
            observation_not_granted.permission,
        )

    def test_multiple_authorities_do_not_require_multiple_permissions(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            len(observation.authorities),
            2,
        )
        self.assertIsNotNone(observation.permission)

    def test_permission_can_be_one_result_of_multiple_authority_inputs(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertIn(authority_a, observation.authorities)
        self.assertIn(authority_b, observation.authorities)
        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

    def test_authority_order_is_not_assumed_to_be_permission_order(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation_a = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_b = PermissionObservation(
            authorities=[authority_b, authority_a],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            set(observation_a.authorities),
            set(observation_b.authorities),
        )
        self.assertEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_permission_observation_can_exist_without_execution(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )
        self.assertFalse(execution_occurred)

    def test_authority_plurality_does_not_create_execution(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertEqual(
            len(observation.authorities),
            2,
        )

    def test_permission_can_remain_stable_when_authority_set_changes(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")
        authority_c = Authority("authority_c")

        observation_a = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        observation_b = PermissionObservation(
            authorities=[authority_a, authority_c],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation_a.authorities,
            observation_b.authorities,
        )
        self.assertEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_multiple_authorities_do_not_prove_resolution_is_required(self):
        authority_a = Authority("authority_a")
        authority_b = Authority("authority_b")

        observation = PermissionObservation(
            authorities=[authority_a, authority_b],
            context="context_a",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        # Important:
        # This experiment intentionally does NOT introduce
        # a Resolution object or Resolution identity.
        resolution_required = False

        self.assertFalse(resolution_required)


if __name__ == "__main__":
    unittest.main()