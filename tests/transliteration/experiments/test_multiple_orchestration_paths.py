import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()
    DEFERRED = auto()


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
class ExperimentalPathObservation:
    request: ExperimentalExecutionRequest
    path: ExperimentalOrchestrationPath
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalMinimalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestMultipleOrchestrationPaths(unittest.TestCase):

    def test_request_can_use_direct_orchestration_path(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.path,
            ExperimentalOrchestrationPath.DIRECT,
        )

    def test_request_can_use_queued_orchestration_path(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.path,
            ExperimentalOrchestrationPath.QUEUED,
        )

    def test_request_can_use_deferred_orchestration_path(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DEFERRED,
            decision=ExperimentalAdmissionDecision.DEFERRED,
        )

        self.assertEqual(
            observation.path,
            ExperimentalOrchestrationPath.DEFERRED,
        )

    def test_same_request_can_be_observed_through_multiple_paths(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        direct = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        queued = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            direct.request.request_id,
            queued.request.request_id,
        )

        self.assertNotEqual(
            direct.path,
            queued.path,
        )

    def test_admission_decision_can_be_preserved_across_paths(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        direct = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        queued = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            direct.decision,
            queued.decision,
        )

    def test_different_paths_can_produce_different_decisions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_path_does_not_equal_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            observation.path.name,
            observation.decision.name,
        )

    def test_admission_decision_does_not_require_path_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertFalse(
            hasattr(observation, "path")
        )

    def test_minimal_observation_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalMinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

    def test_path_is_not_required_to_represent_rejection(self):
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
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_path_is_not_required_to_represent_acceptance(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_multiple_paths_do_not_change_execution_boundary(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        direct = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.DIRECT,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        queued = ExperimentalPathObservation(
            request=request,
            path=ExperimentalOrchestrationPath.QUEUED,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = None

        self.assertEqual(
            direct.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            queued.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()