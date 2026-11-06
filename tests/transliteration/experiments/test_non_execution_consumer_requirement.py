import unittest
from enum import Enum


class ExecutionState(Enum):
    NOT_EXECUTED = "not_executed"
    SUCCESS = "success"
    FAILED = "failed"


class NonExecutionReason(Enum):
    PRECONDITION_NOT_MET = "precondition_not_met"
    EXECUTION_BLOCKED = "execution_blocked"
    UNKNOWN = "unknown"


class ExecutionResult:
    def __init__(
        self,
        state,
        non_execution_reason=None,
    ):
        self.state = state
        self.non_execution_reason = non_execution_reason


class BasicConsumer:
    """Consumer that only needs execution state."""

    @staticmethod
    def handle(result):
        if result.state == ExecutionState.NOT_EXECUTED:
            return "execution_did_not_start"

        if result.state == ExecutionState.SUCCESS:
            return "execution_succeeded"

        if result.state == ExecutionState.FAILED:
            return "execution_failed"

        return "unknown_state"


class ReasonAwareConsumer:
    """Consumer that uses the non-execution reason when available."""

    @staticmethod
    def handle(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return "not_a_non_execution_result"

        if result.non_execution_reason is None:
            return "reason_unavailable"

        if (
            result.non_execution_reason
            == NonExecutionReason.UNKNOWN
        ):
            return "reason_unknown"

        if (
            result.non_execution_reason
            == NonExecutionReason.PRECONDITION_NOT_MET
        ):
            return "precondition_not_met"

        if (
            result.non_execution_reason
            == NonExecutionReason.EXECUTION_BLOCKED
        ):
            return "execution_blocked"

        return "unrecognized_reason"


class TestNonExecutionConsumerRequirement(unittest.TestCase):

    def test_basic_consumer_does_not_require_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        self.assertEqual(
            BasicConsumer.handle(result),
            "execution_did_not_start",
        )

    def test_basic_consumer_works_with_known_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            BasicConsumer.handle(result),
            "execution_did_not_start",
        )

    def test_reason_aware_consumer_detects_known_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            ReasonAwareConsumer.handle(result),
            "precondition_not_met",
        )

    def test_reason_aware_consumer_detects_explicit_unknown(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            ReasonAwareConsumer.handle(result),
            "reason_unknown",
        )

    def test_reason_aware_consumer_detects_absent_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        self.assertEqual(
            ReasonAwareConsumer.handle(result),
            "reason_unavailable",
        )

    def test_absent_reason_and_unknown_have_different_consumer_meaning(self):
        result_none = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        result_unknown = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertNotEqual(
            ReasonAwareConsumer.handle(result_none),
            ReasonAwareConsumer.handle(result_unknown),
        )

    def test_reason_is_not_required_for_basic_execution_handling(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
        )

        interpretation = BasicConsumer.handle(result)

        self.assertEqual(
            interpretation,
            "execution_did_not_start",
        )

    def test_reason_aware_consumer_can_continue_without_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        interpretation = ReasonAwareConsumer.handle(result)

        self.assertEqual(
            interpretation,
            "reason_unavailable",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)