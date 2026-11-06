import unittest
from enum import Enum


class ExecutionState(Enum):
    NOT_EXECUTED = "not_executed"
    SUCCESS = "success"
    FAILED = "failed"


class NonExecutionReason(Enum):
    PRECONDITION_NOT_MET = "precondition_not_met"
    EXECUTION_BLOCKED = "execution_blocked"
    REQUEST_CANCELLED = "request_cancelled"
    UNKNOWN = "unknown"


class ExecutionResult:
    def __init__(self, state, non_execution_reason=None):
        self.state = state
        self.non_execution_reason = non_execution_reason


class ConsumerDecision:
    """
    Experimental consumer decisions.

    These functions intentionally model consumer behavior,
    not a production API.
    """

    @staticmethod
    def execution_outcome(result):
        if result.state == ExecutionState.SUCCESS:
            return "use_output"

        if result.state == ExecutionState.FAILED:
            return "handle_failure"

        if result.state == ExecutionState.NOT_EXECUTED:
            return "handle_non_execution"

        return "unknown"

    @staticmethod
    def retry_decision(result):
        """
        Deliberately conservative:
        execution state alone cannot distinguish
        retryable and non-retryable non-execution causes.
        """
        if result.state != ExecutionState.NOT_EXECUTED:
            return "not_applicable"

        if result.non_execution_reason is None:
            return "cannot_determine"

        if result.non_execution_reason == (
            NonExecutionReason.PRECONDITION_NOT_MET
        ):
            return "do_not_retry_yet"

        if result.non_execution_reason == (
            NonExecutionReason.EXECUTION_BLOCKED
        ):
            return "do_not_retry"

        if result.non_execution_reason == (
            NonExecutionReason.REQUEST_CANCELLED
        ):
            return "do_not_retry"

        if result.non_execution_reason == NonExecutionReason.UNKNOWN:
            return "cannot_determine"

        return "cannot_determine"


class TestConsumerDecisionSufficiency(unittest.TestCase):

    # ---------------------------------------------------------
    # Decision A — execution-level decisions
    # ---------------------------------------------------------

    def test_execution_state_is_sufficient_for_success(self):
        result = ExecutionResult(ExecutionState.SUCCESS)

        self.assertEqual(
            ConsumerDecision.execution_outcome(result),
            "use_output",
        )

    def test_execution_state_is_sufficient_for_failure(self):
        result = ExecutionResult(ExecutionState.FAILED)

        self.assertEqual(
            ConsumerDecision.execution_outcome(result),
            "handle_failure",
        )

    def test_execution_state_is_sufficient_for_non_execution(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            ConsumerDecision.execution_outcome(result),
            "handle_non_execution",
        )

    # ---------------------------------------------------------
    # Decision B — reason-dependent decisions
    # ---------------------------------------------------------

    def test_precondition_reason_changes_retry_decision(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertEqual(
            ConsumerDecision.retry_decision(result),
            "do_not_retry_yet",
        )

    def test_blocked_reason_changes_retry_decision(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.EXECUTION_BLOCKED,
        )

        self.assertEqual(
            ConsumerDecision.retry_decision(result),
            "do_not_retry",
        )

    def test_cancelled_reason_changes_retry_decision(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.REQUEST_CANCELLED,
        )

        self.assertEqual(
            ConsumerDecision.retry_decision(result),
            "do_not_retry",
        )

    def test_none_reason_prevents_reason_dependent_decision(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            ConsumerDecision.retry_decision(result),
            "cannot_determine",
        )

    def test_unknown_reason_prevents_reason_dependent_decision(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            ConsumerDecision.retry_decision(result),
            "cannot_determine",
        )

    def test_same_state_can_require_different_consumer_decisions(self):
        results = [
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.PRECONDITION_NOT_MET,
            ),
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.EXECUTION_BLOCKED,
            ),
            ExecutionResult(
                ExecutionState.NOT_EXECUTED,
                NonExecutionReason.REQUEST_CANCELLED,
            ),
        ]

        decisions = {
            ConsumerDecision.retry_decision(result)
            for result in results
        }

        self.assertEqual(
            decisions,
            {
                "do_not_retry_yet",
                "do_not_retry",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)