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


@dataclass
class MutableAdmissionDecision:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ImmutableAdmissionDecisionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionMutation(unittest.TestCase):

    def test_mutable_model_can_change_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        decision = MutableAdmissionDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        decision.decision = ExperimentalAdmissionDecision.ACCEPTED

        self.assertEqual(
            decision.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_mutation_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        decision = MutableAdmissionDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        original_request_id = request.request_id

        decision.decision = ExperimentalAdmissionDecision.ACCEPTED

        self.assertEqual(
            decision.request.request_id,
            original_request_id,
        )

    def test_immutable_observations_preserve_original_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            second.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_immutable_observations_preserve_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_mutable_model_cannot_preserve_previous_value_in_same_instance(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        decision = MutableAdmissionDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        decision.decision = ExperimentalAdmissionDecision.ACCEPTED

        self.assertEqual(
            decision.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            decision.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_immutable_model_can_preserve_previous_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            second.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_multiple_immutable_observations_form_history(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            3,
        )

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
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_mutation_and_observation_are_semantically_distinguishable(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        mutable = MutableAdmissionDecision(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        immutable = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        mutable.decision = ExperimentalAdmissionDecision.ACCEPTED

        self.assertEqual(
            mutable.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            immutable.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_new_observation_does_not_require_mutating_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request,
            second.request,
        )

    def test_observation_model_does_not_require_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        execution = None

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertIsNone(execution)

    def test_observation_model_does_not_require_decision_id(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ImmutableAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.request.request_id,
            request.request_id,
        )

    def test_mutable_model_is_not_required_to_represent_multiple_decisions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ImmutableAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            observations[0].request.request_id,
            observations[1].request.request_id,
        )

        self.assertNotEqual(
            observations[0].decision,
            observations[1].decision,
        )


if __name__ == "__main__":
    unittest.main()