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


class ExperimentalExecutor:

    def __init__(self, execution_mode="success"):
        self.execution_mode = execution_mode

    def execute(self, text):

        if self.execution_mode == "known_reason":
            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.PRECONDITION_NOT_MET
                ),
                diagnostic="Required precondition is not satisfied",
            )

        if self.execution_mode == "unknown_none":
            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=None,
                diagnostic="Execution did not begin; reason unavailable",
            )

        if self.execution_mode == "unknown_explicit":
            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=NonExecutionReason.UNKNOWN,
                diagnostic="Execution did not begin; reason could not be determined",
            )

        if self.execution_mode == "capability_unavailable":
            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.CAPABILITY_UNAVAILABLE
                ),
                diagnostic="Transliteration capability is not available",
            )

        if self.execution_mode == "execution_error":
            return ExecutionResult(
                state=ExecutionState.FAILED,
                failure=FailureClassification.EXECUTION_ERROR,
                diagnostic="Unexpected transliteration failure",
            )

        if self.execution_mode == "invalid_combination":
            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                failure=FailureClassification.EXECUTION_ERROR,
                diagnostic="Invalid experimental state combination",
            )

        return ExecutionResult(
            state=ExecutionState.SUCCESS,
            output=f"[Transliterated] {text}",
        )


class TestNonExecutionReasonRequirement(unittest.TestCase):

    def test_known_reason(self):
        result = ExperimentalExecutor("known_reason").execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertIsNone(result.failure)

    def test_unknown_reason_as_none(self):
        result = ExperimentalExecutor("unknown_none").execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(result.non_execution_reason)
        self.assertIsNone(result.failure)

    def test_unknown_reason_explicit(self):
        result = ExperimentalExecutor(
            "unknown_explicit"
        ).execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.UNKNOWN,
        )

        self.assertIsNone(result.failure)

    def test_capability_unavailable(self):
        result = ExperimentalExecutor(
            "capability_unavailable"
        ).execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.CAPABILITY_UNAVAILABLE,
        )

        self.assertIsNone(result.failure)

    def test_success_control(self):
        result = ExperimentalExecutor().execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.SUCCESS,
        )

        self.assertIsNone(result.non_execution_reason)
        self.assertIsNone(result.failure)
        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )

    def test_failure_control(self):
        result = ExperimentalExecutor(
            "execution_error"
        ).execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.FAILED,
        )

        self.assertIsNone(result.non_execution_reason)

        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )

    def test_invalid_not_executed_failure_combination(self):
        result = ExperimentalExecutor(
            "invalid_combination"
        ).execute("hanacaraka")

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(result.non_execution_reason)

        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)