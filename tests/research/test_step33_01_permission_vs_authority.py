import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class PermissionObservation:
    authority: str
    permission: ExecutionPermission


class TestPermissionVsAuthority(unittest.TestCase):

    def test_permission_can_be_granted_by_an_authority(self):
        observation = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.authority,
            "authority-A",
        )

    def test_same_permission_value_can_be_associated_with_different_authorities(self):
        first = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        second = PermissionObservation(
            authority="authority-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.permission,
            second.permission,
        )

        self.assertNotEqual(
            first.authority,
            second.authority,
        )

    def test_authority_and_permission_are_distinct_dimensions(self):
        observation = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.authority,
            "authority-A",
        )

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            type(observation.authority),
            type(observation.permission),
        )

    def test_permission_value_does_not_identify_authority(self):
        first = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        second = PermissionObservation(
            authority="authority-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.permission,
            second.permission,
        )

        self.assertNotEqual(
            first.authority,
            second.authority,
        )

    def test_authority_identity_does_not_identify_permission_value(self):
        first = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        second = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            first.authority,
            second.authority,
        )

        self.assertNotEqual(
            first.permission,
            second.permission,
        )

    def test_permission_can_change_while_authority_remains_same(self):
        before = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.authority,
            after.authority,
        )

        self.assertNotEqual(
            before.permission,
            after.permission,
        )

    def test_authority_can_change_while_permission_remains_same(self):
        before = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        after = PermissionObservation(
            authority="authority-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            before.authority,
            after.authority,
        )

        self.assertEqual(
            before.permission,
            after.permission,
        )

    def test_permission_is_not_execution_occurrence(self):
        observation = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(execution_occurred)

    def test_authority_is_not_execution_occurrence(self):
        observation = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            observation.authority,
            "authority-A",
        )

        self.assertFalse(execution_occurred)

    def test_permission_identity_can_be_distinct_from_authority_identity(self):
        permission_id = "permission-001"
        authority_id = "authority-001"

        self.assertNotEqual(
            permission_id,
            authority_id,
        )

    def test_same_authority_can_support_multiple_permission_observations(self):
        observations = [
            PermissionObservation(
                authority="authority-A",
                permission=ExecutionPermission.NOT_GRANTED,
            ),
            PermissionObservation(
                authority="authority-A",
                permission=ExecutionPermission.GRANTED,
            ),
        ]

        self.assertEqual(
            observations[0].authority,
            observations[1].authority,
        )

        self.assertNotEqual(
            observations[0].permission,
            observations[1].permission,
        )

    def test_same_permission_can_be_observed_with_multiple_authorities(self):
        observations = [
            PermissionObservation(
                authority="authority-A",
                permission=ExecutionPermission.GRANTED,
            ),
            PermissionObservation(
                authority="authority-B",
                permission=ExecutionPermission.GRANTED,
            ),
        ]

        self.assertEqual(
            observations[0].permission,
            observations[1].permission,
        )

        self.assertNotEqual(
            observations[0].authority,
            observations[1].authority,
        )

    def test_authority_change_does_not_necessarily_mean_permission_change(self):
        before = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        after = PermissionObservation(
            authority="authority-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            before.authority,
            after.authority,
        )

        self.assertEqual(
            before.permission,
            after.permission,
        )

    def test_permission_change_does_not_necessarily_mean_authority_change(self):
        before = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            before.authority,
            after.authority,
        )

        self.assertNotEqual(
            before.permission,
            after.permission,
        )

    def test_permission_and_authority_are_semantically_distinguishable(self):
        observation = PermissionObservation(
            authority="authority-A",
            permission=ExecutionPermission.GRANTED,
        )

        authority_semantics = "source_or_basis_of_authority"
        permission_semantics = "permission_state"

        self.assertNotEqual(
            authority_semantics,
            permission_semantics,
        )


if __name__ == "__main__":
    unittest.main()