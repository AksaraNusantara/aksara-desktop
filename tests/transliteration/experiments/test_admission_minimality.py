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
class MinimalAdmissionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionMinimality(unittest.TestCase):

    def test_minimal_model_can_represent_one_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.001",
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_model_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

    def test_minimal_model_can_represent_rejection_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution_id = None

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution_id)

    def test_minimal_model_can_represent_acceptance_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution_id)

    def test_minimal_model_can_represent_multiple_admission_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

    def test_minimal_model_preserves_same_request_across_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        request_ids = {
            observation.request.request_id
            for observation in observations
        }

        self.assertEqual(
            request_ids,
            {"req.006"},
        )

    def test_minimal_model_can_represent_reconsideration(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_minimal_model_does_not_require_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.008",
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_model_can_preserve_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.operation.operation_id,
            "op.transliterate",
        )

    def test_minimal_model_can_represent_multiple_decisions_for_one_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            MinimalAdmissionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        decisions = [
            observation.decision
            for observation in observations
        ]

        self.assertEqual(
            len(decisions),
            3,
        )

        self.assertEqual(
            decisions[-1],
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_model_can_coexist_with_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = "exec.001"

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

        self.assertEqual(
            execution_id,
            "exec.001",
        )

    def test_minimal_model_does_not_conflate_decision_with_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = MinimalAdmissionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_state = "NOT_STARTED"

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution_state,
            "NOT_STARTED",
        )


if __name__ == "__main__":
    unittest.main()