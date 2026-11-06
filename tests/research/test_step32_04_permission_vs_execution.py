import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class Scenario:
    permission: ExecutionPermission
    execution_occurred: bool


class TestPermissionVsExecution(unittest.TestCase):

    def test_permission_granted_can_exist_without_execution(self):
        scenario = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=False,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(
            scenario.execution_occurred,
        )

    def test_permission_granted_can_coexist_with_execution(self):
        scenario = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=True,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertTrue(
            scenario.execution_occurred,
        )

    def test_permission_not_granted_can_exist_without_execution(self):
        scenario = Scenario(
            permission=ExecutionPermission.NOT_GRANTED,
            execution_occurred=False,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertFalse(
            scenario.execution_occurred,
        )

    def test_permission_and_execution_are_distinct_dimensions(self):
        granted = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=False,
        )

        executed = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=True,
        )

        self.assertEqual(
            granted.permission,
            executed.permission,
        )

        self.assertNotEqual(
            granted.execution_occurred,
            executed.execution_occurred,
        )

    def test_execution_occurrence_does_not_define_permission_value(self):
        scenario = Scenario(
            permission=ExecutionPermission.NOT_GRANTED,
            execution_occurred=False,
        )

        self.assertFalse(
            scenario.execution_occurred,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_granted_permission_does_not_create_execution_identity(self):
        permission_id = "permission-001"
        execution_id = None

        self.assertEqual(
            permission_id,
            "permission-001",
        )

        self.assertIsNone(
            execution_id,
        )

    def test_execution_identity_can_appear_after_permission(self):
        permission_id = "permission-001"
        execution_id = "execution-001"

        self.assertNotEqual(
            permission_id,
            execution_id,
        )

    def test_permission_can_precede_execution_temporally(self):
        observations = [
            ("permission", ExecutionPermission.GRANTED),
            ("execution", False),
        ]

        self.assertEqual(
            observations[0][0],
            "permission",
        )

        self.assertEqual(
            observations[1][0],
            "execution",
        )

    def test_execution_can_remain_absent_after_permission(self):
        permission = ExecutionPermission.GRANTED
        execution_exists = False

        self.assertEqual(
            permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(
            execution_exists,
        )

    def test_permission_granted_is_not_execution_state(self):
        permission = ExecutionPermission.GRANTED
        execution_state = "not_started"

        self.assertEqual(
            permission,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            execution_state,
            "not_started",
        )

    def test_execution_occurrence_is_not_permission(self):
        execution_occurred = True
        permission = ExecutionPermission.GRANTED

        self.assertTrue(
            execution_occurred,
        )

        self.assertEqual(
            permission,
            ExecutionPermission.GRANTED,
        )

    def test_permission_can_remain_stable_while_execution_changes(self):
        before = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=False,
        )

        after = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=True,
        )

        self.assertEqual(
            before.permission,
            after.permission,
        )

        self.assertNotEqual(
            before.execution_occurred,
            after.execution_occurred,
        )

    def test_execution_occurrence_is_an_event_not_permission(self):
        permission = ExecutionPermission.GRANTED
        execution_event = "execution_started"

        self.assertEqual(
            permission,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            execution_event,
            "execution_started",
        )

    def test_granted_permission_does_not_guarantee_execution(self):
        scenario = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=False,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(
            scenario.execution_occurred,
        )

    def test_permission_and_execution_have_separate_semantics(self):
        scenario = Scenario(
            permission=ExecutionPermission.GRANTED,
            execution_occurred=True,
        )

        permission_semantics = "authorization_or_permission"
        execution_semantics = "actual_occurrence"

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertTrue(
            scenario.execution_occurred,
        )

        self.assertNotEqual(
            permission_semantics,
            execution_semantics,
        )


if __name__ == "__main__":
    unittest.main()