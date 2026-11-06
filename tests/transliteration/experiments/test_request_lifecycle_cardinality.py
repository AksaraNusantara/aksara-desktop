import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalLifecycleEvent(Enum):
    CREATED = auto()
    ACCEPTED = auto()
    QUEUED = auto()
    DEFERRED = auto()
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


class TestRequestLifecycleCardinality(unittest.TestCase):

    def test_one_request_can_have_one_lifecycle_observation(self):
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
            event=ExperimentalLifecycleEvent.CREATED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.001",
        )

    def test_one_request_can_have_multiple_lifecycle_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
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
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
        ]

        self.assertEqual(
            len(observations),
            3,
        )

    def test_multiple_observations_preserve_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
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
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
        ]

        request_ids = {
            observation.request.request_id
            for observation in observations
        }

        self.assertEqual(
            request_ids,
            {"req.003"},
        )

    def test_one_request_can_be_observed_in_multiple_distinct_conditions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        events = [
            ExperimentalLifecycleEvent.CREATED,
            ExperimentalLifecycleEvent.ACCEPTED,
            ExperimentalLifecycleEvent.QUEUED,
            ExperimentalLifecycleEvent.DEFERRED,
        ]

        observations = [
            ExperimentalLifecycleObservation(
                request=request,
                event=event,
            )
            for event in events
        ]

        self.assertEqual(
            len(observations),
            4,
        )

    def test_lifecycle_observation_does_not_require_execution(self):
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
            event=ExperimentalLifecycleEvent.QUEUED,
        )

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertEqual(
            observation.request.request_id,
            "req.005",
        )

    def test_one_request_can_have_multiple_pre_execution_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.ACCEPTED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.DEFERRED,
            ),
        ]

        execution_id = None

        self.assertEqual(
            len(observations),
            3,
        )

        self.assertIsNone(execution_id)

    def test_one_request_can_be_queued_more_than_once(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.DEFERRED,
            ),
            ExperimentalLifecycleObservation(
                request=request,
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
        ]

        queued_events = [
            observation
            for observation in observations
            if observation.event
            == ExperimentalLifecycleEvent.QUEUED
        ]

        self.assertEqual(
            len(queued_events),
            2,
        )

    def test_repeated_lifecycle_event_does_not_create_new_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.QUEUED,
        )

        second = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.QUEUED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_lifecycle_cardinality_is_not_execution_cardinality(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
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
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
        ]

        execution_ids = []

        self.assertGreater(
            len(observations),
            1,
        )

        self.assertEqual(
            execution_ids,
            [],
        )

    def test_lifecycle_observations_can_represent_progression(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
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
                event=ExperimentalLifecycleEvent.QUEUED,
            ),
        ]

        event_sequence = [
            observation.event
            for observation in observations
        ]

        self.assertEqual(
            event_sequence,
            [
                ExperimentalLifecycleEvent.CREATED,
                ExperimentalLifecycleEvent.ACCEPTED,
                ExperimentalLifecycleEvent.QUEUED,
            ],
        )

    def test_request_identity_can_survive_terminal_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalLifecycleObservation(
            request=request,
            event=ExperimentalLifecycleEvent.CANCELLED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.011",
        )

    def test_lifecycle_history_can_be_empty(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = []

        self.assertEqual(
            len(observations),
            0,
        )

        self.assertEqual(
            request.request_id,
            "req.012",
        )


if __name__ == "__main__":
    unittest.main()