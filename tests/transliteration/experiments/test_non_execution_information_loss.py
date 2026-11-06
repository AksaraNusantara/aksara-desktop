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
        diagnostic=None,
    ):
        self.state = state
        self.non_execution_reason = non_execution_reason
        self.diagnostic = diagnostic


class ConsumerInterpretation:
    """
    Experimental consumer interpretation.

    This is intentionally not a production API.
    """

    @staticmethod
    def interpret(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return "not_a_non_execution_result"

        if result.non_execution_reason is None:
            return "reason_value_absent"

        if result.non_execution_reason == NonExecutionReason.UNKNOWN:
            return "reason_explicitly_unknown"

        return "reason_known"


class TestNonExecutionInformationLoss(unittest.TestCase):

    def test_known_reason_is_observable(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        interpretation = ConsumerInterpretation.interpret(result)

        self.assertEqual(
            interpretation,
            "reason_known",
        )

    def test_none_is_observable_as_absence(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        interpretation = ConsumerInterpretation.interpret(result)

        self.assertEqual(
            interpretation,
            "reason_value_absent",
        )

    def test_unknown_is_observable_as_explicit_unknown(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        interpretation = ConsumerInterpretation.interpret(result)

        self.assertEqual(
            interpretation,
            "reason_explicitly_unknown",
        )

    def test_none_and_unknown_produce_different_information(self):
        result_none = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        result_unknown = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        interpretation_none = ConsumerInterpretation.interpret(
            result_none
        )

        interpretation_unknown = ConsumerInterpretation.interpret(
            result_unknown
        )

        self.assertNotEqual(
            interpretation_none,
            interpretation_unknown,
        )

    def test_known_and_unknown_are_distinguishable(self):
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
            ConsumerInterpretation.interpret(known),
            ConsumerInterpretation.interpret(unknown),
        )

    def test_none_does_not_imply_unknown(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        self.assertNotEqual(
            ConsumerInterpretation.interpret(result),
            "reason_explicitly_unknown",
        )

    def test_unknown_does_not_imply_known_reason(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=NonExecutionReason.UNKNOWN,
        )

        self.assertNotEqual(
            ConsumerInterpretation.interpret(result),
            "reason_known",
        )

    def test_execution_state_remains_not_executed(self):
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