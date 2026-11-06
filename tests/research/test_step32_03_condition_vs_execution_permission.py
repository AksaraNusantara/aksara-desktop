import unittest
from dataclasses import dataclass
from enum import Enum


class PreExecutionCondition(Enum):
    READY = "ready"
    NOT_READY = "not_ready"


class ExecutionPermission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


@dataclass(frozen=True)
class Scenario:
    condition: PreExecutionCondition
    permission: ExecutionPermission


class TestConditionVsExecutionPermission(unittest.TestCase):

    def test_ready_can_coexist_with_permission_granted(self):
        scenario = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

    def test_ready_can_coexist_with_permission_not_granted(self):
        scenario = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_not_ready_can_coexist_with_permission_not_granted(self):
        scenario = Scenario(
            condition=PreExecutionCondition.NOT_READY,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_not_ready_can_coexist_with_permission_granted(self):
        scenario = Scenario(
            condition=PreExecutionCondition.NOT_READY,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.NOT_READY,
        )

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

    def test_ready_does_not_intrinsically_equal_permission_granted(self):
        ready = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            ready.condition,
            PreExecutionCondition.READY,
        )

        self.assertEqual(
            ready.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_permission_does_not_intrinsically_equal_ready(self):
        granted = Scenario(
            condition=PreExecutionCondition.NOT_READY,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            granted.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            granted.condition,
            PreExecutionCondition.NOT_READY,
        )

    def test_condition_and_permission_have_distinct_value_spaces(self):
        self.assertNotEqual(
            set(PreExecutionCondition),
            set(ExecutionPermission),
        )

    def test_condition_change_does_not_require_permission_change(self):
        first = Scenario(
            condition=PreExecutionCondition.NOT_READY,
            permission=ExecutionPermission.GRANTED,
        )

        second = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            first.condition,
            second.condition,
        )

        self.assertEqual(
            first.permission,
            second.permission,
        )

    def test_permission_change_does_not_require_condition_change(self):
        first = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        second = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            first.condition,
            second.condition,
        )

        self.assertNotEqual(
            first.permission,
            second.permission,
        )

    def test_ready_does_not_mean_execution_occurred(self):
        scenario = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.NOT_GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            scenario.condition,
            PreExecutionCondition.READY,
        )

        self.assertFalse(execution_occurred)

    def test_permission_granted_does_not_mean_execution_occurred(self):
        scenario = Scenario(
            condition=PreExecutionCondition.NOT_READY,
            permission=ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(execution_occurred)

    def test_condition_and_permission_can_be_observed_independently(self):
        observations = [
            ("condition", PreExecutionCondition.READY),
            ("permission", ExecutionPermission.NOT_GRANTED),
        ]

        self.assertEqual(
            observations[0][0],
            "condition",
        )

        self.assertEqual(
            observations[1][0],
            "permission",
        )

    def test_permission_is_not_execution_identity(self):
        permission_id = "permission-001"
        execution_id = "execution-001"

        self.assertNotEqual(
            permission_id,
            execution_id,
        )

    def test_permission_granted_does_not_force_immediate_execution(self):
        scenario = Scenario(
            condition=PreExecutionCondition.READY,
            permission=ExecutionPermission.GRANTED,
        )

        execution_started = False

        self.assertEqual(
            scenario.permission,
            ExecutionPermission.GRANTED,
        )

        self.assertFalse(execution_started)


if __name__ == "__main__":
    unittest.main()