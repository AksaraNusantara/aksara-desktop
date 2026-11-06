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


class ExperimentalDeferredState(Enum):
    DEFERRED = auto()


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
class ExperimentalDeferredRequest:
    request: ExperimentalExecutionRequest
    state: ExperimentalDeferredState


@dataclass(frozen=True)
class ExperimentalQueueEntry:
    request: ExperimentalExecutionRequest
    state: ExperimentalQueueState


@dataclass(frozen=True)
class ExperimentalExecution:
    execution_id: str
    operation: ExperimentalOperation


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    execution: ExperimentalExecution | None
    state: ExperimentalExecutionState


class TestDeferredExecutionBoundary(unittest.TestCase):

    def test_accepted_request_can_exist_without_execution(self):
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

    def test_deferred_request_can_exist_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        execution = None

        self.assertEqual(
            deferred.state,
            ExperimentalDeferredState.DEFERRED,
        )

        self.assertIsNone(execution)

    def test_deferred_is_not_execution_state(self):
        self.assertNotIn(
            "DEFERRED",
            {
                state.name
                for state in ExperimentalExecutionState
            },
        )

    def test_deferred_is_not_admission_decision(self):
        self.assertNotEqual(
            ExperimentalDeferredState.DEFERRED,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            ExperimentalDeferredState.DEFERRED,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_deferred_request_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        self.assertEqual(
            deferred.request.request_id,
            "req.005",
        )

    def test_deferred_request_preserves_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        self.assertEqual(
            deferred.request.operation.operation_id,
            "op.transliterate",
        )

    def test_deferred_request_can_later_produce_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.007",
            operation=operation,
        )

        self.assertEqual(
            deferred.request.operation.operation_id,
            execution.operation.operation_id,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.007",
        )

    def test_queued_request_and_deferred_request_can_be_distinguished(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        queued = ExperimentalQueueEntry(
            request=request,
            state=ExperimentalQueueState.QUEUED,
        )

        self.assertNotEqual(
            deferred.state,
            queued.state,
        )

    def test_deferred_and_queued_do_not_create_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
        )

        queued = ExperimentalQueueEntry(
            request=request,
            state=ExperimentalQueueState.QUEUED,
        )

        deferred_execution = None
        queued_execution = None

        self.assertEqual(
            deferred.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            queued.request.request_id,
            request.request_id,
        )

        self.assertIsNone(deferred_execution)
        self.assertIsNone(queued_execution)

    def test_deferred_execution_does_not_require_not_executed_state_as_a_new_state(self):
        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(
            result.execution
        )

    def test_execution_semantics_remain_unchanged_after_deferred_period(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
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
            deferred.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.011",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_deferred_boundary_can_be_conceptually_separated_from_execution(self):
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

        deferred = ExperimentalDeferredRequest(
            request=request,
            state=ExperimentalDeferredState.DEFERRED,
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
            deferred.request.request_id,
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