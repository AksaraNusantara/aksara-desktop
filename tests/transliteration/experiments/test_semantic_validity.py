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
    ):
        self.state = state
        self.output = output
        self.non_execution_reason = non_execution_reason
        self.failure = failure


class SemanticAssessment:
    """
    Experimental semantic assessment only.

    This is NOT a production validator.
    """

    @staticmethod
    def execution_started(result):
        if result.state == ExecutionState.NOT_EXECUTED:
            return False

        if result.state in (
            ExecutionState.SUCCESS,
            ExecutionState.FAILED,
        ):
            return True

        raise AssertionError("Unknown execution state")

    @staticmethod
    def reason_is_semantically_relevant(result):
        return (
            result.state == ExecutionState.NOT_EXECUTED
            and result.non_execution_reason is not None
        )

    @staticmethod
    def failure_is_semantically_relevant(result):
        return (
            result.state == ExecutionState.FAILED
            and result.failure is not None
        )


class TestSemanticValidity(unittest.TestCase):

    def test_not_executed_means_execution_did_not_start(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertFalse(
            SemanticAssessment.execution_started(result)
        )

    def test_success_means_execution_started(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
        )

        self.assertTrue(
            SemanticAssessment.execution_started(result)
        )

    def test_failed_means_execution_started(self):
        result = ExecutionResult(
            state=ExecutionState.FAILED,
            failure=FailureClassification.EXECUTION_ERROR,
        )

        self.assertTrue(
            SemanticAssessment.execution_started(result)
        )

    def test_non_execution_reason_is_relevant_to_not_executed(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.CAPABILITY_UNAVAILABLE
            ),
        )

        self.assertTrue(
            SemanticAssessment.reason_is_semantically_relevant(result)
        )

    def test_failure_is_relevant_to_failed(self):
        result = ExecutionResult(
            state=ExecutionState.FAILED,
            failure=FailureClassification.EXECUTION_ERROR,
        )

        self.assertTrue(
            SemanticAssessment.failure_is_semantically_relevant(result)
        )

    def test_failure_is_not_semantically_relevant_to_not_executed(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            failure=FailureClassification.EXECUTION_ERROR,
        )

        self.assertFalse(
            SemanticAssessment.failure_is_semantically_relevant(result)
        )

    def test_reason_is_not_semantically_relevant_to_success(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertFalse(
            SemanticAssessment.reason_is_semantically_relevant(result)
        )

    def test_failure_is_not_semantically_relevant_to_success(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
            output="hasil transliterasi",
            failure=FailureClassification.EXECUTION_ERROR,
        )

        self.assertFalse(
            SemanticAssessment.failure_is_semantically_relevant(result)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)