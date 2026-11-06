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


class FailureClassification(Enum):
    INVALID_INPUT = "invalid_input"
    EXECUTION_ERROR = "execution_error"


class ExecutionResult:
    def __init__(
        self,
        state,
        output=None,
        non_execution_reason=None,
        failure=None,
        diagnostic=None,
    ):
        self.state = state
        self.output = output
        self.non_execution_reason = non_execution_reason
        self.failure = failure
        self.diagnostic = diagnostic


class TestNonExecutionResultInvariants(unittest.TestCase):

    def test_success_has_no_reason_and_no_failure(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
        )

        self.assertEqual(result.state, ExecutionState.SUCCESS)
        self.assertIsNone(result.non_execution_reason)
        self.assertIsNone(result.failure)

    def test_failed_has_failure_but_no_non_execution_reason(self):
        result = ExecutionResult(
            state=ExecutionState.FAILED,
            failure=FailureClassification.EXECUTION_ERROR,
            diagnostic="Execution failed",
        )

        self.assertEqual(result.state, ExecutionState.FAILED)
        self.assertIsNone(result.non_execution_reason)
        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )

    def test_not_executed_with_reason_has_no_failure(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.PRECONDITION_NOT_MET,
            diagnostic="Precondition is not satisfied",
        )

        self.assertEqual(result.state, ExecutionState.NOT_EXECUTED)
        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )
        self.assertIsNone(result.failure)

    def test_not_executed_without_reason_has_no_failure(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            diagnostic="Reason unavailable",
        )

        self.assertEqual(result.state, ExecutionState.NOT_EXECUTED)
        self.assertIsNone(result.non_execution_reason)
        self.assertIsNone(result.failure)

    def test_not_executed_with_reason_and_failure_is_representable(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.EXECUTION_BLOCKED,
            failure=FailureClassification.EXECUTION_ERROR,
            diagnostic="Experimental mixed state",
        )

        self.assertEqual(result.state, ExecutionState.NOT_EXECUTED)
        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.EXECUTION_BLOCKED,
        )
        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )

    def test_failed_with_reason_is_representable(self):
        result = ExecutionResult(
            state=ExecutionState.FAILED,
            non_execution_reason=NonExecutionReason.PRECONDITION_NOT_MET,
            failure=FailureClassification.EXECUTION_ERROR,
            diagnostic="Experimental mixed state",
        )

        self.assertEqual(result.state, ExecutionState.FAILED)
        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )
        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )

    def test_success_with_reason_is_representable(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
            non_execution_reason=NonExecutionReason.UNKNOWN,
            diagnostic="Experimental mixed state",
        )

        self.assertEqual(result.state, ExecutionState.SUCCESS)
        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.UNKNOWN,
        )
        self.assertIsNone(result.failure)

    def test_success_with_failure_is_representable(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
            failure=FailureClassification.EXECUTION_ERROR,
            diagnostic="Experimental mixed state",
        )

        self.assertEqual(result.state, ExecutionState.SUCCESS)
        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)