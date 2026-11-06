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
class ExperimentalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalOrchestrationObservation:
    request: ExperimentalExecutionRequest
    admission_decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionOwnership(unittest.TestCase):

    def test_admission_observation_can_hold_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_orchestration_observation_can_produce_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            orchestration.admission_decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_same_request_can_be_represented_in_both_models(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            orchestration.request.request_id,
        )

    def test_decision_semantics_can_be_preserved_without_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.admission_decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_decision_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution_id = None

        self.assertEqual(
            orchestration.admission_decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution_id)

    def test_admission_and_orchestration_can_express_same_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.decision,
            orchestration.admission_decision,
        )

    def test_decision_is_distinct_from_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.decision.name,
            request.request_id,
        )

    def test_decision_is_distinct_from_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.decision.name,
            operation.operation_id,
        )

    def test_orchestration_can_be_observed_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution = None

        self.assertEqual(
            orchestration.request.request_id,
            request.request_id,
        )

        self.assertIsNone(execution)

    def test_admission_decision_can_change_between_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.admission_decision,
            second.admission_decision,
        )

    def test_request_identity_remains_stable_when_decision_changes(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_admission_decision_does_not_define_execution_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            admission_decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_state = "NOT_STARTED"

        self.assertEqual(
            orchestration.admission_decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution_state,
            "NOT_STARTED",
        )


if __name__ == "__main__":
    unittest.main()