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


class TestAdmissionDecisionReordering(unittest.TestCase):

    def test_reordering_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertEqual(
            sequence[0].request.request_id,
            reordered[0].request.request_id,
        )

        self.assertEqual(
            sequence[1].request.request_id,
            reordered[1].request.request_id,
        )

    def test_reordering_preserves_number_of_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
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
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertEqual(
            len(sequence),
            len(reordered),
        )

    def test_reordering_preserves_decision_multiset(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
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

        reordered = list(reversed(sequence))

        original_values = sorted(
            observation.decision.name
            for observation in sequence
        )

        reordered_values = sorted(
            observation.decision.name
            for observation in reordered
        )

        self.assertEqual(
            original_values,
            reordered_values,
        )

    def test_reordering_changes_first_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertNotEqual(
            sequence[0].decision,
            reordered[0].decision,
        )

    def test_reordering_changes_last_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertNotEqual(
            sequence[-1].decision,
            reordered[-1].decision,
        )

    def test_reordering_changes_sequence_equality(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertNotEqual(
            sequence,
            reordered,
        )

    def test_reordering_does_not_mutate_original_sequence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        original_first = sequence[0]
        original_last = sequence[-1]

        reordered = list(reversed(sequence))

        self.assertIs(
            sequence[0],
            original_first,
        )

        self.assertIs(
            sequence[-1],
            original_last,
        )

        self.assertIsNot(
            sequence,
            reordered,
        )

    def test_reordering_preserves_observation_objects(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [first, second]
        reordered = list(reversed(sequence))

        self.assertIs(
            reordered[0],
            second,
        )

        self.assertIs(
            reordered[1],
            first,
        )

    def test_reordering_does_not_require_decision_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [first, second]
        reordered = list(reversed(sequence))

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            second.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            reordered[0].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            reordered[1].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_transition_direction_depends_on_order(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence_a = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        sequence_b = list(reversed(sequence_a))

        transition_a = (
            sequence_a[0].decision,
            sequence_a[1].decision,
        )

        transition_b = (
            sequence_b[0].decision,
            sequence_b[1].decision,
        )

        self.assertNotEqual(
            transition_a,
            transition_b,
        )

    def test_order_independent_information_can_be_extracted(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reordered = list(reversed(sequence))

        def decision_multiset(observations):
            return sorted(
                observation.decision.name
                for observation in observations
            )

        self.assertEqual(
            decision_multiset(sequence),
            decision_multiset(reordered),
        )

    def test_order_dependent_information_is_distinguishable(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        sequence_a = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        sequence_b = list(reversed(sequence_a))

        first_a = sequence_a[0].decision
        first_b = sequence_b[0].decision

        last_a = sequence_a[-1].decision
        last_b = sequence_b[-1].decision

        self.assertNotEqual(
            first_a,
            first_b,
        )

        self.assertNotEqual(
            last_a,
            last_b,
        )


if __name__ == "__main__":
    unittest.main()