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


class ContractAssessment:

    @staticmethod
    def has_execution_outcome(result):
        return result.state is not None

    @staticmethod
    def has_non_execution_reason(result):
        if result.state != ExecutionState.NOT_EXECUTED:
            return True

        return result.non_execution_reason is not None

    @staticmethod
    def is_fully_described(result):
        if not ContractAssessment.has_execution_outcome(result):
            return False

        if result.state == ExecutionState.NOT_EXECUTED:
            return (
                result.non_execution_reason is not None
            )

        return True


class TestNonExecutionContractCompleteness(unittest.TestCase):

    def test_known_reason_is_fully_described(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertTrue(
            ContractAssessment.is_fully_described(result)
        )

    def test_explicit_unknown_is_fully_described(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.UNKNOWN
            ),
        )

        self.assertTrue(
            ContractAssessment.is_fully_described(result)
        )

    def test_none_is_not_fully_described(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        self.assertFalse(
            ContractAssessment.is_fully_described(result)
        )

    def test_known_reason_is_available_to_contract(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.EXECUTION_BLOCKED
            ),
        )

        self.assertTrue(
            ContractAssessment.has_non_execution_reason(result)
        )

    def test_unknown_reason_is_available_to_contract(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                NonExecutionReason.UNKNOWN
            ),
        )

        self.assertTrue(
            ContractAssessment.has_non_execution_reason(result)
        )

    def test_absent_reason_is_detectable_as_incomplete(self):
        result = ExecutionResult(
            state=ExecutionState.NOT_EXECUTED,
            non_execution_reason=None,
        )

        self.assertFalse(
            ContractAssessment.has_non_execution_reason(result)
        )

    def test_success_does_not_require_non_execution_reason(self):
        result = ExecutionResult(
            state=ExecutionState.SUCCESS,
        )

        self.assertTrue(
            ContractAssessment.is_fully_described(result)
        )

    def test_failed_does_not_require_non_execution_reason(self):
        result = ExecutionResult(
            state=ExecutionState.FAILED,
        )

        self.assertTrue(
            ContractAssessment.is_fully_described(result)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)