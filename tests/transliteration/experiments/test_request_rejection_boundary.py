import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalNonExecutionReason(Enum):
    ADMISSION_REJECTED = auto()


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalAdmissionResult:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalExecution:
    execution_id: str
    operation: ExperimentalOperation


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    execution: ExperimentalExecution | None
    state: ExperimentalExecutionState
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


class TestRequestRejectionBoundary(unittest.TestCase):

    def test_rejection_is_an_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_rejection_does_not_create_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution)

    def test_rejection_can_be_represented_by_not_executed(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertEqual(
            request.request_id,
            "req.003",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_rejection_reason_preserves_specific_information(self):
        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.ADMISSION_REJECTED,
        )

    def test_rejection_is_not_execution_failure(self):
        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertNotEqual(
            result.state,
            ExperimentalExecutionState.FAILED,
        )

    def test_rejection_is_not_execution_success(self):
        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertNotEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_rejection_and_execution_state_are_separate_dimensions(self):
        admission = ExperimentalAdmissionDecision.REJECTED

        execution_state = ExperimentalExecutionState.NOT_EXECUTED

        self.assertEqual(
            admission,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            execution_state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertNotEqual(
            admission,
            execution_state,
        )

    def test_rejected_request_preserves_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.request.operation.operation_id,
            "op.transliterate",
        )

    def test_rejected_request_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.008",
        )

    def test_rejection_does_not_require_rejected_execution_state(self):
        execution_states = {
            ExperimentalExecutionState.SUCCESS,
            ExperimentalExecutionState.FAILED,
            ExperimentalExecutionState.NOT_EXECUTED,
        }

        self.assertNotIn(
            "REJECTED",
            {state.name for state in execution_states},
        )

    def test_rejection_information_can_survive_without_admission_object(self):
        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.ADMISSION_REJECTED,
        )

    def test_accepted_and_rejected_requests_share_execution_model(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        accepted_request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected_request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        accepted_admission = ExperimentalAdmissionResult(
            request=accepted_request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        rejected_admission = ExperimentalAdmissionResult(
            request=rejected_request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.010",
            operation=operation,
        )

        accepted_result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        rejected_result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertEqual(
            accepted_admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            rejected_admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            accepted_result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            rejected_result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_rejection_does_not_change_request_operation_relationship(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.ADMISSION_REJECTED
            ),
        )

        self.assertEqual(
            admission.request.operation,
            operation,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )


if __name__ == "__main__":
    unittest.main()