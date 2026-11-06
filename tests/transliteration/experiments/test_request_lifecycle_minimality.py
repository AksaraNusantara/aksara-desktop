import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


class ExperimentalOrchestrationEvent(Enum):
    CREATED = auto()
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
class ExperimentalAdmission:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalOrchestrationEventRecord:
    request: ExperimentalExecutionRequest
    event: ExperimentalOrchestrationEvent


class TestRequestLifecycleMinimality(unittest.TestCase):

    def test_request_identity_requires_no_request_state(self):
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

    def test_request_can_exist_before_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = None

        self.assertIsNone(admission)
        self.assertEqual(
            request.request_id,
            "req.002",
        )

    def test_accepted_lifecycle_requires_only_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_rejected_lifecycle_requires_only_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_queued_lifecycle_requires_only_orchestration_event(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.QUEUED,
        )

        self.assertEqual(
            event.event,
            ExperimentalOrchestrationEvent.QUEUED,
        )

    def test_deferred_lifecycle_requires_only_orchestration_event(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.DEFERRED,
        )

        self.assertEqual(
            event.event,
            ExperimentalOrchestrationEvent.DEFERRED,
        )

    def test_cancelled_lifecycle_requires_only_orchestration_event(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.CANCELLED,
        )

        self.assertEqual(
            event.event,
            ExperimentalOrchestrationEvent.CANCELLED,
        )

    def test_complete_pre_execution_lifecycle_without_request_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        events = [
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.CREATED,
            ),
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.QUEUED,
            ),
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.DEFERRED,
            ),
        ]

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            [event.event for event in events],
            [
                ExperimentalOrchestrationEvent.CREATED,
                ExperimentalOrchestrationEvent.QUEUED,
                ExperimentalOrchestrationEvent.DEFERRED,
            ],
        )

    def test_terminal_pre_execution_lifecycle_without_request_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        terminal_events = {
            ExperimentalOrchestrationEvent.CANCELLED,
        }

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.CANCELLED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIn(
            event.event,
            terminal_events,
        )

    def test_repeated_queue_defer_queue_without_request_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        events = [
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.QUEUED,
            ),
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.DEFERRED,
            ),
            ExperimentalOrchestrationEventRecord(
                request=request,
                event=ExperimentalOrchestrationEvent.QUEUED,
            ),
        ]

        self.assertEqual(
            [event.event for event in events],
            [
                ExperimentalOrchestrationEvent.QUEUED,
                ExperimentalOrchestrationEvent.DEFERRED,
                ExperimentalOrchestrationEvent.QUEUED,
            ],
        )

    def test_lifecycle_information_preserves_request_identity_without_request_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.QUEUED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.011",
        )

        self.assertEqual(
            event.request.request_id,
            "req.011",
        )

    def test_lifecycle_model_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.DEFERRED,
        )

        execution_id = None

        self.assertEqual(
            admission.request.request_id,
            "req.012",
        )

        self.assertEqual(
            event.request.request_id,
            "req.012",
        )

        self.assertIsNone(execution_id)

    def test_minimal_model_contains_no_request_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.013",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        event = ExperimentalOrchestrationEventRecord(
            request=request,
            event=ExperimentalOrchestrationEvent.QUEUED,
        )

        model_types = {
            type(request),
            type(admission),
            type(event),
        }

        self.assertNotIn(
            "ExperimentalRequestState",
            {
                model_type.__name__
                for model_type in model_types
            },
        )


if __name__ == "__main__":
    unittest.main()