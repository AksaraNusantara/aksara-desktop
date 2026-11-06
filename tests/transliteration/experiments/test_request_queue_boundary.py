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


class ExperimentalQueueState(Enum):
    QUEUED = auto()


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
class ExperimentalQueueEntry:
    request: ExperimentalExecutionRequest
    queue_state: ExperimentalQueueState


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


class TestRequestQueueBoundary(unittest.TestCase):

    def test_accepted_request_can_exist_before_execution(self):
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

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertIsNone(execution)

    def test_queue_entry_can_reference_request_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        self.assertEqual(
            queue_entry.request.request_id,
            "req.002",
        )

        execution = None

        self.assertIsNone(execution)

    def test_queue_state_is_not_execution_state(self):
        self.assertNotIn(
            "QUEUED",
            {
                state.name
                for state in ExperimentalExecutionState
            },
        )

    def test_queue_state_is_not_admission_decision(self):
        self.assertNotEqual(
            ExperimentalQueueState.QUEUED,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            ExperimentalQueueState.QUEUED,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_queued_request_has_no_execution_identity_yet(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        self.assertEqual(
            queue_entry.request.request_id,
            "req.004",
        )

        execution_id = None

        self.assertIsNone(execution_id)

    def test_queued_request_can_later_produce_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation=operation,
        )

        self.assertEqual(
            queue_entry.request.operation.operation_id,
            execution.operation.operation_id,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.005",
        )

    def test_queue_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        self.assertEqual(
            queue_entry.request.request_id,
            request.request_id,
        )

    def test_queue_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        self.assertEqual(
            queue_entry.request.operation.operation_id,
            "op.transliterate",
        )

    def test_accepted_queued_and_executed_are_distinguishable_concepts(self):
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

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.008",
            operation=operation,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            queue_entry.queue_state,
            ExperimentalQueueState.QUEUED,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.008",
        )

    def test_queue_is_not_required_to_create_not_executed_result(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            request.request_id,
            "req.009",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    def test_request_can_be_deferred_without_changing_execution_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
        )

        result_before_execution = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            queue_entry.request.request_id,
            request.request_id,
        )

        self.assertIsNone(
            result_before_execution.execution
        )

    def test_execution_result_remains_independent_of_queue_representation(self):
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
            result.execution.execution_id,
            "exec.011",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_request_queue_execution_boundary_can_be_conceptually_separated(self):
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

        queue_entry = ExperimentalQueueEntry(
            request=request,
            queue_state=ExperimentalQueueState.QUEUED,
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
            admission.request.request_id,
            "req.012",
        )

        self.assertEqual(
            queue_entry.request.request_id,
            "req.012",
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