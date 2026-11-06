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
class ExperimentalAdmissionDecisionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class ExperimentalDecisionHistory:
    def __init__(self, observations):
        self.observations = list(observations)


class TestAdmissionDecisionHistoryMinimality(unittest.TestCase):

    def test_single_observation_needs_no_history_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

    def test_multiple_observations_can_be_represented_as_plain_collection(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

    def test_plain_collection_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        for observation in observations:
            self.assertEqual(
                observation.request.request_id,
                request.request_id,
            )

    def test_plain_collection_preserves_decision_values(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_history_wrapper_does_not_add_required_decision_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        history = ExperimentalDecisionHistory(observations)

        self.assertEqual(
            history.observations,
            observations,
        )

    def test_history_wrapper_can_be_removed_without_losing_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        history = ExperimentalDecisionHistory(observations)

        recovered = list(history.observations)

        self.assertEqual(
            recovered,
            observations,
        )

    def test_no_history_wrapper_is_needed_for_empty_history(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = []

        self.assertEqual(
            observations,
            [],
        )

        self.assertEqual(
            request.request_id,
            "req.007",
        )

    def test_no_history_wrapper_is_needed_for_single_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_plain_collection_can_preserve_reconsideration_sequence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observations[2].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_history_object_does_not_create_execution_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        history = ExperimentalDecisionHistory(observations)

        execution = None

        self.assertEqual(
            len(history.observations),
            2,
        )

        self.assertIsNone(execution)

    def test_decision_history_does_not_require_decision_id(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            observations[0].request.request_id,
            observations[1].request.request_id,
        )

    def test_minimal_model_preserves_principal_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertEqual(
            observations[0].request.request_id,
            request.request_id,
        )

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )


if __name__ == "__main__":
    unittest.main()