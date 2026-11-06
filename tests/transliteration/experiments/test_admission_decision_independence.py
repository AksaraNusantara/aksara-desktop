import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


class ExperimentalOrchestrationPath(Enum):
    DIRECT = auto()
    QUEUED = auto()
    DEFERRED = auto()


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
    path: ExperimentalOrchestrationPath
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalMinimalDecision:
    decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionIndependence(unittest.TestCase):

    def test_decision_can_exist_with_direct_path(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_decision_can_exist_with_queued_path(self):
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
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_decision_can_exist_with_deferred_path(self):
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
            path=ExperimentalOrchestrationPath.DEFERRED,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_same_decision_can_be_represented_without_path(self):
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
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            orchestration.decision,
            admission.decision,
        )

    def test_decision_can_be_represented_as_minimal_information(self):
        decision = ExperimentalMinimalDecision(
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            decision.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_request_identity_is_not_required_to_define_decision_value(self):
        decision = ExperimentalMinimalDecision(
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            decision.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_path_does_not_change_the_meaning_of_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        direct = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        queued = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            direct.decision,
            queued.decision,
        )

    def test_orchestration_details_can_be_removed_without_losing_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DEFERRED,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        decision_only = ExperimentalMinimalDecision(
            decision=orchestration.decision,
        )

        self.assertEqual(
            orchestration.decision,
            decision_only.decision,
        )

    def test_admission_observation_does_not_require_orchestration_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        orchestration = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(orchestration)

    def test_orchestration_observation_is_not_identical_to_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        orchestration = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            orchestration.path,
            orchestration.decision,
        )

    def test_decision_can_be_compared_across_different_observation_contexts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        direct = ExperimentalOrchestrationObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        minimal = ExperimentalMinimalDecision(
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            direct.decision,
            admission.decision,
        )

        self.assertEqual(
            admission.decision,
            minimal.decision,
        )

    def test_decision_independence_does_not_create_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()