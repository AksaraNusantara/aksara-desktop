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
class ExperimentalOrchestrationObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalMinimalDecision:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestOrchestrationMinimality(unittest.TestCase):

    def test_orchestration_can_carry_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_admission_observation_can_carry_decision_without_orchestration(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_minimal_model_can_carry_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            minimal.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_orchestration_is_not_required_for_rejection_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            minimal.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_orchestration_is_not_required_for_acceptance_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            minimal.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_same_decision_is_preserved_across_three_models(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.decision,
            admission.decision,
        )

        self.assertEqual(
            admission.decision,
            minimal.decision,
        )

    def test_orchestration_does_not_define_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.request.request_id,
            request.request_id,
        )

    def test_admission_does_not_require_orchestration_identity(self):
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

        self.assertFalse(
            hasattr(admission, "orchestration_id")
        )

    def test_minimal_model_does_not_require_orchestration_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertFalse(
            hasattr(minimal, "orchestration_id")
        )

        self.assertFalse(
            hasattr(minimal, "orchestration_event")
        )

    def test_minimal_model_preserves_request_and_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            minimal.request.request_id,
            "req.010",
        )

        self.assertEqual(
            minimal.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_orchestration_can_be_treated_as_context(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        decision = orchestration.decision

        self.assertEqual(
            decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimality_does_not_create_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        minimal = ExperimentalMinimalDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertEqual(
            minimal.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()