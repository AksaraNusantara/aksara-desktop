import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


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


@dataclass(frozen=True)
class ExperimentalExecutionWithAdmission:
    execution: ExperimentalExecution
    admission: ExperimentalAdmissionDecision


class TestAdmissionExecutionBoundary(unittest.TestCase):

    def test_admission_can_exist_without_execution(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution)

    def test_rejected_admission_has_no_execution(self):
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

    def test_accepted_admission_can_precede_execution(self):
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

        execution = ExperimentalExecution(
            execution_id="exec.003",
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

    def test_admission_decision_is_not_execution_state(self):
        self.assertNotEqual(
            ExperimentalAdmissionDecision.ACCEPTED,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertNotEqual(
            ExperimentalAdmissionDecision.REJECTED,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_execution_can_reference_admission_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation=operation,
        )

        execution_with_admission = ExperimentalExecutionWithAdmission(
            execution=execution,
            admission=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution_with_admission.execution.execution_id,
            "exec.005",
        )

        self.assertEqual(
            execution_with_admission.admission,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_admission_information_does_not_create_new_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.006",
            operation=operation,
        )

        with_admission = ExperimentalExecutionWithAdmission(
            execution=execution,
            admission=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            with_admission.execution.execution_id,
            execution.execution_id,
        )

    def test_same_execution_can_be_described_with_or_without_admission_wrapper(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.007",
            operation=operation,
        )

        plain_result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        wrapped_execution = ExperimentalExecutionWithAdmission(
            execution=execution,
            admission=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            plain_result.execution.execution_id,
            wrapped_execution.execution.execution_id,
        )

    def test_admission_decision_can_be_observed_before_execution(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.008",
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_admission_and_execution_have_different_temporal_positions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionResult(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.009",
            operation=operation,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.009",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.009",
        )

    def test_rejection_can_be_semantically_complete_without_execution(self):
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
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(
            result.execution
        )

    def test_execution_result_can_exist_without_representing_admission_as_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.011",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

        self.assertNotIn(
            "ACCEPTED",
            {
                state.name
                for state in ExperimentalExecutionState
            },
        )

    def test_conceptual_boundary_preserves_all_three_identities(self):
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
            operation.operation_id,
            "op.transliterate",
        )

        self.assertEqual(
            request.request_id,
            "req.012",
        )

        self.assertEqual(
            admission.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.012",
        )

        self.assertEqual(
            result.execution.execution_id,
            execution.execution_id,
        )


if __name__ == "__main__":
    unittest.main()