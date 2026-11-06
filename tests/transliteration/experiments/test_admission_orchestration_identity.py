import unittest
from dataclasses import dataclass
from enum import Enum, auto


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
class ExperimentalAdmissionOccurrence:
    admission_id: str
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalOrchestrationOccurrence:
    orchestration_id: str
    request: ExperimentalExecutionRequest
    admission_decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalMinimalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionOrchestrationIdentity(unittest.TestCase):

    def test_admission_can_have_distinct_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionOccurrence(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.admission_id,
            "adm.001",
        )

    def test_orchestration_can_have_distinct_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.001",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.orchestration_id,
            "orch.001",
        )

    def test_admission_and_orchestration_identities_can_be_distinct(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionOccurrence(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        orchestration = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.001",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.admission_id,
            orchestration.orchestration_id,
        )

    def test_request_identity_remains_distinct_from_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionOccurrence(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            request.request_id,
            admission.admission_id,
        )

    def test_request_identity_remains_distinct_from_orchestration_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.005",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            request.request_id,
            orchestration.orchestration_id,
        )

    def test_same_orchestration_can_produce_multiple_admission_occurrences(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration_id = "orch.006"

        first = ExperimentalAdmissionOccurrence(
            admission_id="adm.006.a",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmissionOccurrence(
            admission_id="adm.006.b",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration_id,
            "orch.006",
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )

    def test_multiple_orchestration_occurrences_can_reference_same_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.007.a",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.007.b",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

        self.assertNotEqual(
            first.orchestration_id,
            second.orchestration_id,
        )

    def test_admission_identity_does_not_define_decision_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionOccurrence(
            admission_id="adm.008",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_orchestration_identity_does_not_define_decision_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationOccurrence(
            orchestration_id="orch.009",
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            orchestration.admission_decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_minimal_observation_preserves_admission_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_observation_requires_no_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
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

        self.assertFalse(
            hasattr(observation, "admission_id")
        )

    def test_identity_is_not_required_to_preserve_decision_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.012",
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )


if __name__ == "__main__":
    unittest.main()