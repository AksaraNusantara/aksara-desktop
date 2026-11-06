import unittest
from enum import Enum


class ExecutionState(Enum):
    NOT_EXECUTED = "not_executed"
    SUCCESS = "success"
    FAILED = "failed"


class NonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = "capability_unavailable"
    PRECONDITION_NOT_MET = "precondition_not_met"
    EXECUTION_BLOCKED = "execution_blocked"
    REQUEST_CANCELLED = "request_cancelled"
    UNKNOWN = "unknown"


class ExecutionResult:
    def __init__(
        self,
        state,
        non_execution_reason=None,
        diagnostic=None,
    ):
        self.state = state
        self.non_execution_reason = non_execution_reason
        self.diagnostic = diagnostic


class TestUnknownReasonSemantics(unittest.TestCase):

    def test_known_reason_contains_reason_information(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
            diagnostic="Required precondition is not satisfied",
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertIsNotNone(result.non_execution_reason)

    def test_none_represents_absence_of_reason_value(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
            diagnostic="Execution did not begin",
        )

        self.assertIsNone(result.non_execution_reason)

    def test_unknown_represents_explicit_unknown_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
            diagnostic="Execution did not begin; reason is unknown",
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.UNKNOWN,
        )

    def test_none_and_unknown_are_not_the_same_value(self):
        self.assertIsNone(None)

        self.assertNotEqual(
            None,
            NonExecutionReason.UNKNOWN,
        )

    def test_none_does_not_claim_reason_knowledge(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        reason_known = (
            result.non_execution_reason is not None
        )

        self.assertFalse(reason_known)

    def test_unknown_explicitly_records_unknown_status(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        reason_is_explicitly_unknown = (
            result.non_execution_reason
            == NonExecutionReason.UNKNOWN
        )

        self.assertTrue(reason_is_explicitly_unknown)

    def test_known_reason_is_distinguishable_from_unknown(self):
        known = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.EXECUTION_BLOCKED
            ),
        )

        unknown = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertNotEqual(
            known.non_execution_reason,
            unknown.non_execution_reason,
        )

    def test_unknown_reason_preserves_not_executed_state(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)