import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalLifecycleEvent(Enum):
    CREATED = auto()
    ACCEPTED = auto()
    QUEUED = auto()
    DEFERRED = auto()
    REJECTED = auto()
    CANCELLED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalLifecycleObservation:
    request: ExperimentalExecutionRequest
    event: ExperimentalLifecycleEvent


class TestRequestTerminalState(unittest.TestCase):

    def test_rejected_can_be_observed_as_terminal_condition(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.REJECTED,
        )

        self.assertEqual(
            observation.event,
            ExperimentalLifecycleEvent.REJECTED,
        )

    def test_cancelled_can_be_observed_as_terminal_condition(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            observation.event,
            ExperimentalLifecycleEvent.CANCELLED,
        )

    def test_rejected_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.REJECTED,
        )

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertEqual(
            observation.request.request_id,
            "req.003",
        )

    def test_cancelled_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertEqual(
            observation.request.request_id,
            "req.004",
        )

    def test_terminal_observation_does_not_destroy_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            request.request_id,
            observation.request.request_id,
        )

    def test_terminal_observation_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.REJECTED,
        )

        self.assertEqual(
            observation.request.operation.operation_id,
            "op.transliterate",
        )

    def test_terminal_condition_is_not_execution_state(self):
        execution_states = {
            "SUCCESS",
            "FAILED",
            "NOT_EXECUTED",
        }

        self.assertNotIn(
            "REJECTED",
            execution_states,
        )

        self.assertNotIn(
            "CANCELLED",
            execution_states,
        )

    def test_terminal_condition_can_coexist_with_not_executed_result(self):
        execution_state = "NOT_EXECUTED"

        lifecycle_event = ExperimentalLifecycleEvent.REJECTED

        self.assertEqual(
            execution_state,
            "NOT_EXECUTED",
        )

        self.assertEqual(
            lifecycle_event,
            ExperimentalLifecycleEvent.REJECTED,
        )

    def test_terminality_is_an_interpretation_of_lifecycle_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        terminal_events = {
            ExperimentalLifecycleEvent.REJECTED,
            ExperimentalLifecycleEvent.CANCELLED,
        }

        self.assertIn(
            observation.event,
            terminal_events,
        )

    def test_request_identity_remains_valid_after_terminal_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        terminal = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            terminal.request.request_id,
            "req.009",
        )

    def test_terminal_observation_can_be_stored_as_history(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        history = [
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.CREATED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.ACCEPTED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.CANCELLED,
            ),
        ]

        self.assertEqual(
            history[-1].event,
            ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            history[-1].request.request_id,
            "req.010",
        )

    def test_terminal_observation_does_not_imply_execution_occurred(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        history = [
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.CREATED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.CANCELLED,
            ),
        ]

        execution_ids = []

        self.assertEqual(
            history[-1].event,
            ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            execution_ids,
            [],
        )

    def test_terminality_does_not_require_request_state_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.REJECTED,
        )

        terminal_events = {
            ExperimentalLifecycleEvent.REJECTED,
            ExperimentalLifecycleEvent.CANCELLED,
        }

        is_terminal = observation.event in terminal_events

        self.assertTrue(is_terminal)

        self.assertEqual(
            request.request_id,
            "req.012",
        )


if __name__ == "__main__":
    unittest.main()