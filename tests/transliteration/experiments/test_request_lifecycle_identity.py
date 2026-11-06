import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalRequestLifecycle(Enum):
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
class ExperimentalRequestLifecycleObservation:
    request: ExperimentalExecutionRequest
    lifecycle: ExperimentalRequestLifecycle


class TestRequestLifecycleIdentity(unittest.TestCase):

    def test_request_has_identity_at_creation(self):
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

    def test_request_identity_is_preserved_when_accepted(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.002",
        )

    def test_request_identity_is_preserved_when_queued(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.QUEUED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.003",
        )

    def test_request_identity_is_preserved_when_deferred(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.DEFERRED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.004",
        )

    def test_request_identity_is_preserved_when_rejected(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.REJECTED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.005",
        )

    def test_request_identity_is_preserved_when_cancelled(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.CANCELLED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.006",
        )

    def test_same_request_can_have_multiple_lifecycle_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        created = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.CREATED,
        )

        accepted = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.ACCEPTED,
        )

        queued = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.QUEUED,
        )

        self.assertEqual(
            created.request.request_id,
            accepted.request.request_id,
        )

        self.assertEqual(
            accepted.request.request_id,
            queued.request.request_id,
        )

    def test_lifecycle_observation_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.DEFERRED,
        )

        self.assertEqual(
            observation.request.operation.operation_id,
            "op.transliterate",
        )

    def test_lifecycle_is_distinct_from_execution_state(self):
        class ExperimentalExecutionState(Enum):
            SUCCESS = auto()
            FAILED = auto()
            NOT_EXECUTED = auto()

        self.assertNotIn(
            "QUEUED",
            {
                state.name
                for state in ExperimentalExecutionState
            },
        )

        self.assertNotIn(
            "DEFERRED",
            {
                state.name
                for state in ExperimentalExecutionState
            },
        )

    def test_lifecycle_identity_is_independent_of_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            observation.request.request_id,
            "req.010",
        )

        self.assertIsNone(execution_id)

    def test_same_request_identity_can_reach_terminal_lifecycle(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        accepted = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.ACCEPTED,
        )

        cancelled = ExperimentalRequestLifecycleObservation(
            request=request,
            lifecycle=ExperimentalRequestLifecycle.CANCELLED,
        )

        self.assertEqual(
            accepted.request.request_id,
            cancelled.request.request_id,
        )

    def test_request_lifecycle_model_preserves_request_identity_across_multiple_conditions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalRequestLifecycleObservation(
                request=request,
                lifecycle=ExperimentalRequestLifecycle.CREATED,
            ),
            ExperimentalRequestLifecycleObservation(
                request=request,
                lifecycle=ExperimentalRequestLifecycle.ACCEPTED,
            ),
            ExperimentalRequestLifecycleObservation(
                request=request,
                lifecycle=ExperimentalRequestLifecycle.QUEUED,
            ),
            ExperimentalRequestLifecycleObservation(
                request=request,
                lifecycle=ExperimentalRequestLifecycle.DEFERRED,
            ),
        ]

        request_ids = {
            observation.request.request_id
            for observation in observations
        }

        self.assertEqual(
            request_ids,
            {"req.012"},
        )


if __name__ == "__main__":
    unittest.main()