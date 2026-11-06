import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


class ExperimentalOrchestrationEventType(Enum):
    CREATED = auto()
    QUEUED = auto()
    DEFERRED = auto()
    CANCELLED = auto()
    ADMISSION_EVALUATED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalOrchestrationEvent:
    event_type: ExperimentalOrchestrationEventType
    request: ExperimentalExecutionRequest


@dataclass(frozen=True)
class ExperimentalAdmissionEvent:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalOrchestrationAdmissionEvent:
    event_type: ExperimentalOrchestrationEventType
    request: ExperimentalExecutionRequest
    admission_decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalMinimalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionOrchestrationEvent(unittest.TestCase):

    def test_orchestration_event_can_exist_without_admission_event(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.QUEUED,
            request=request,
        )

        self.assertEqual(
            event.event_type,
            ExperimentalOrchestrationEventType.QUEUED,
        )

    def test_admission_event_can_exist_as_distinct_occurrence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission_event = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission_event.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_same_request_can_have_orchestration_and_admission_events(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration_event = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
        )

        admission_event = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration_event.request.request_id,
            admission_event.request.request_id,
        )

    def test_orchestration_event_type_does_not_equal_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration_event = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
        )

        admission_event = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            orchestration_event.event_type.name,
            admission_event.decision.name,
        )

    def test_admission_decision_can_be_carried_by_orchestration_event(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationAdmissionEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            event.admission_decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_admission_decision_can_be_represented_without_event_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_multiple_orchestration_events_can_surround_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.QUEUED,
            request=request,
        )

        second = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
        )

        third = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.DEFERRED,
            request=request,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

        self.assertEqual(
            second.request.request_id,
            third.request.request_id,
        )

    def test_admission_decision_can_be_observed_between_orchestration_events(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        before = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.QUEUED,
            request=request,
        )

        admission = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        after = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
        )

        self.assertEqual(
            before.request.request_id,
            admission.request.request_id,
        )

        self.assertEqual(
            admission.request.request_id,
            after.request.request_id,
        )

    def test_orchestration_event_does_not_require_execution_occurrence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        event = ExperimentalOrchestrationEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
        )

        execution = None

        self.assertEqual(
            event.request.request_id,
            request.request_id,
        )

        self.assertIsNone(execution)

    def test_admission_event_does_not_require_execution_occurrence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        admission_event = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution = None

        self.assertEqual(
            admission_event.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution)

    def test_admission_decision_is_preserved_across_event_models(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admission_event = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        orchestration_event = ExperimentalOrchestrationAdmissionEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        minimal = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission_event.decision,
            orchestration_event.admission_decision,
        )

        self.assertEqual(
            orchestration_event.admission_decision,
            minimal.decision,
        )

    def test_event_distinction_is_not_proof_of_architectural_necessity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        separate = ExperimentalAdmissionEvent(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        combined = ExperimentalOrchestrationAdmissionEvent(
            event_type=ExperimentalOrchestrationEventType.ADMISSION_EVALUATED,
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        minimal = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            separate.decision,
            combined.admission_decision,
        )

        self.assertEqual(
            combined.admission_decision,
            minimal.decision,
        )


if __name__ == "__main__":
    unittest.main()