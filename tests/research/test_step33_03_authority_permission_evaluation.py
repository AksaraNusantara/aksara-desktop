import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class PermissionObservation:
    authority: str
    context: str
    permission: ExecutionPermission


class TestAuthorityPermissionEvaluation(unittest.TestCase):

    def test_same_authority_can_have_different_permissions(self):
        first = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = PermissionObservation(
            authority="authority-A",
            context="context-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.authority, second.authority)
        self.assertNotEqual(first.permission, second.permission)

    def test_context_can_change_permission_with_same_authority(self):
        before = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        after = PermissionObservation(
            authority="authority-A",
            context="context-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(before.authority, after.authority)
        self.assertNotEqual(before.context, after.context)
        self.assertNotEqual(before.permission, after.permission)

    def test_same_context_can_have_different_permissions(self):
        first = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.authority, second.authority)
        self.assertEqual(first.context, second.context)
        self.assertNotEqual(first.permission, second.permission)

    def test_authority_alone_does_not_identify_permission(self):
        observations = [
            PermissionObservation(
                authority="authority-A",
                context="context-A",
                permission=ExecutionPermission.NOT_GRANTED,
            ),
            PermissionObservation(
                authority="authority-A",
                context="context-B",
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

    def test_context_alone_does_not_identify_permission(self):
        observations = [
            PermissionObservation(
                authority="authority-A",
                context="context-A",
                permission=ExecutionPermission.NOT_GRANTED,
            ),
            PermissionObservation(
                authority="authority-B",
                context="context-A",
                permission=ExecutionPermission.GRANTED,
            ),
        ]

        self.assertEqual(
            observations[0].context,
            observations[1].context,
        )

        self.assertNotEqual(
            observations[0].permission,
            observations[1].permission,
        )

    def test_authority_and_context_can_remain_stable_while_permission_changes(self):
        first = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.authority, second.authority)
        self.assertEqual(first.context, second.context)
        self.assertNotEqual(first.permission, second.permission)

    def test_permission_is_an_evaluation_result_in_this_model(self):
        observation = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        inputs = (
            observation.authority,
            observation.context,
        )

        result = observation.permission

        self.assertEqual(len(inputs), 2)
        self.assertEqual(result, ExecutionPermission.GRANTED)

    def test_permission_result_is_not_identical_to_authority(self):
        observation = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation.authority,
            observation.permission,
        )

    def test_permission_result_is_not_identical_to_context(self):
        observation = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation.context,
            observation.permission,
        )

    def test_same_authority_can_support_multiple_permission_observations(self):
        observations = [
            PermissionObservation(
                authority="authority-A",
                context="context-A",
                permission=ExecutionPermission.NOT_GRANTED,
            ),
            PermissionObservation(
                authority="authority-A",
                context="context-B",
                permission=ExecutionPermission.GRANTED,
            ),
            PermissionObservation(
                authority="authority-A",
                context="context-C",
                permission=ExecutionPermission.NOT_GRANTED,
            ),
        ]

        self.assertTrue(
            all(
                observation.authority == "authority-A"
                for observation in observations
            )
        )

        self.assertEqual(
            observations[0].permission,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observations[1].permission,
            ExecutionPermission.GRANTED,
        )

    def test_permission_change_does_not_require_authority_change(self):
        first = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = PermissionObservation(
            authority="authority-A",
            context="context-B",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.authority, second.authority)

    def test_permission_change_does_not_require_context_identity_change(self):
        first = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = PermissionObservation(
            authority="authority-B",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(first.context, second.context)

    def test_permission_is_not_execution_occurrence(self):
        observation = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(execution_occurred)

    def test_authority_and_context_are_possible_inputs_without_being_permission(self):
        observation = PermissionObservation(
            authority="authority-A",
            context="context-A",
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(observation.authority, "authority-A")
        self.assertEqual(observation.context, "context-A")
        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation.authority,
            observation.permission,
        )

        self.assertNotEqual(
            observation.context,
            observation.permission,
        )


if __name__ == "__main__":
    unittest.main()