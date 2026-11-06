import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalRequestState(Enum):
    QUEUED = auto()
    DEFERRED = auto()
    CANCELLED = auto()


class ExperimentalOrchestrationEvent(Enum):
    REQUEST_QUEUED = auto()
    REQUEST_DEFERRED = auto()
    REQUEST_CANCELLED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalOrchestrationObservation:
    request: ExperimentalExecutionRequest
    event: ExperimentalOrchestrationEvent


class TestRequestStateVsOrchestrationEvent(unittest.TestCase):

    def test_request_exists_without_orchestration_event(self):
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

    def test_queued_event_does_not_create_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.002",
        )

    def test_deferred_event_does_not_create_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_DEFERRED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.003",
        )

    def test_cancelled_event_does_not_create_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_CANCELLED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.004",
        )

    def test_orchestration_event_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        self.assertEqual(
            observation.request.operation.operation_id,
            "op.transliterate",
        )

    def test_orchestration_event_is_distinct_from_request_state(self):
        request_state = ExperimentalRequestState.QUEUED
        orchestration_event = (
            ExperimentalOrchestrationEvent.REQUEST_QUEUED
        )

        self.assertNotEqual(
            request_state.name,
            orchestration_event.name,
        )

    def test_multiple_orchestration_events_preserve_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalOrchestrationObservation(
                request=request,
                event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
            ),
            ExperimentalOrchestrationObservation(
                request=request,
                event=ExperimentalOrchestrationEvent.REQUEST_DEFERRED,
            ),
            ExperimentalOrchestrationObservation(
                request=request,
                event=ExperimentalOrchestrationEvent.REQUEST_CANCELLED,
            ),
        ]

        request_ids = {
            observation.request.request_id
            for observation in observations
        }

        self.assertEqual(
            request_ids,
            {"req.006"},
        )

    def test_orchestration_event_can_exist_without_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_DEFERRED,
        )

        execution_id = None

        self.assertEqual(
            observation.request.request_id,
            "req.007",
        )

        self.assertIsNone(execution_id)

    def test_queued_event_does_not_mean_execution_started(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        execution_started = False

        self.assertEqual(
            observation.event,
            ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        self.assertFalse(execution_started)

    def test_deferred_event_does_not_mean_execution_failed(self):
        execution_states = {
            "SUCCESS",
            "FAILED",
            "NOT_EXECUTED",
        }

        self.assertNotIn(
            "DEFERRED",
            execution_states,
        )

    def test_cancelled_event_can_be_observed_before_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_CANCELLED,
        )

        execution_id = None

        self.assertEqual(
            observation.event,
            ExperimentalOrchestrationEvent.REQUEST_CANCELLED,
        )

        self.assertIsNone(execution_id)

    def test_same_request_can_have_different_orchestration_events(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        queued = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        deferred = ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_DEFERRED,
        )

        self.assertEqual(
            queued.request.request_id,
            deferred.request.request_id,
        )

    def test_event_observation_does_not_mutate_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        ExperimentalOrchestrationObservation(
            request=request,
            event=ExperimentalOrchestrationEvent.REQUEST_QUEUED,
        )

        self.assertEqual(
            request.request_id,
            original_request_id,
        )


if __name__ == "__main__":
    unittest.main()