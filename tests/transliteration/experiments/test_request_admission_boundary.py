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


class TestRequestAdmissionBoundary(unittest.TestCase):

    def test_request_exists_before_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertEqual(
            request.request_id,
            "req.001",
        )

    def test_admission_is_about_request_not_execution(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.002",
        )

    def test_accepted_request_can_have_no_execution_yet(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertIsNone(execution)

    def test_rejected_request_has_no_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
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
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(
            result.execution
        )

    def test_admission_decision_does_not_equal_execution_state(self):
        self.assertNotEqual(
            ExperimentalAdmissionDecision.ACCEPTED,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertNotEqual(
            ExperimentalAdmissionDecision.REJECTED,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_accepted_request_can_transition_to_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation=operation,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution.operation.operation_id,
            request.operation.operation_id,
        )

    def test_rejected_request_can_produce_not_executed_result(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
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
            admission.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_admission_does_not_change_operation_identity(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.operation.operation_id,
            "op.transliterate",
        )

    def test_multiple_requests_can_have_different_admission_decisions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_1 = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        request_2 = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission_1 = ExperimentalAdmissionResult(
            request=request_1,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admission_2 = ExperimentalAdmissionResult(
            request=request_2,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission_1.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission_2.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_admission_result_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.010",
        )

        execution = None

        self.assertIsNone(execution)

    def test_execution_identity_only_appears_after_execution_exists(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.011",
            operation=operation,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.011",
        )

    def test_admission_boundary_can_be_conceptually_separated(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.012",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            request.request_id,
            "req.012",
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.012",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )


if __name__ == "__main__":
    unittest.main()