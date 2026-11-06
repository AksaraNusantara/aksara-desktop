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


class StateOnlyConsumer:
    @staticmethod
    def consume(result):
        if result.state == ExecutionState.NOT_EXECUTED:
            return "handle_non_execution"

        if result.state == ExecutionState.SUCCESS:
            return "use_output"

        if result.state == ExecutionState.FAILED:
            return "handle_failure"

        return "unknown"


class ReasonAwareConsumer:
    @staticmethod
    def consume(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return "reason_not_applicable"

        if result.non_execution_reason is None:
            return "reason_not_available"

        if result.non_execution_reason == NonExecutionReason.UNKNOWN:
            return "reason_unknown"

        return result.non_execution_reason.value


class StrictReasonDependentConsumer:
    """
    This consumer explicitly requires a known reason
    before it can perform its decision.
    """

    @staticmethod
    def can_decide(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return True

        if result.non_execution_reason is None:
            return False

        if result.non_execution_reason == NonExecutionReason.UNKNOWN:
            return False

        return True


class TestReasonAvailabilityContract(unittest.TestCase):

    # ---------------------------------------------------------
    # 1. State-only consumer
    # ---------------------------------------------------------

    def test_state_only_consumer_accepts_known_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertEqual(
            StateOnlyConsumer.consume(result),
            "handle_non_execution",
        )

    def test_state_only_consumer_accepts_unknown_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            StateOnlyConsumer.consume(result),
            "handle_non_execution",
        )

    def test_state_only_consumer_accepts_absent_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            StateOnlyConsumer.consume(result),
            "handle_non_execution",
        )

    # ---------------------------------------------------------
    # 2. Reason-aware consumer
    # ---------------------------------------------------------

    def test_reason_aware_consumer_uses_known_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.EXECUTION_BLOCKED,
        )

        self.assertEqual(
            ReasonAwareConsumer.consume(result),
            "execution_blocked",
        )

    def test_reason_aware_consumer_distinguishes_unknown(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertEqual(
            ReasonAwareConsumer.consume(result),
            "reason_unknown",
        )

    def test_reason_aware_consumer_handles_absence(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            ReasonAwareConsumer.consume(result),
            "reason_not_available",
        )

    # ---------------------------------------------------------
    # 3. Strict reason-dependent consumer
    # ---------------------------------------------------------

    def test_strict_consumer_accepts_known_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.PRECONDITION_NOT_MET,
        )

        self.assertTrue(
            StrictReasonDependentConsumer.can_decide(result)
        )

    def test_strict_consumer_rejects_unknown_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            NonExecutionReason.UNKNOWN,
        )

        self.assertFalse(
            StrictReasonDependentConsumer.can_decide(result)
        )

    def test_strict_consumer_rejects_absent_reason(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertFalse(
            StrictReasonDependentConsumer.can_decide(result)
        )

    # ---------------------------------------------------------
    # 4. Contract observation
    # ---------------------------------------------------------

    def test_same_result_can_be_valid_for_one_consumer_and_insufficient_for_another(self):
        result = ExecutionResult(
            ExecutionState.NOT_EXECUTED,
            None,
        )

        self.assertEqual(
            StateOnlyConsumer.consume(result),
            "handle_non_execution",
        )

        self.assertEqual(
            ReasonAwareConsumer.consume(result),
            "reason_not_available",
        )

        self.assertFalse(
            StrictReasonDependentConsumer.can_decide(result)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)