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


class TestAdmissionDecisionArbitraryOrdering(unittest.TestCase):

    def test_arbitrary_order_can_exist_in_representation(self):
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

        ordering_basis = "arbitrary"

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

    def test_arbitrary_order_does_not_change_observation_membership(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        self.assertEqual(
            set(sequence_a),
            set(sequence_b),
        )

    def test_arbitrary_order_does_not_change_request_identity(self):
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
        ]

        for observation in sequence:
            self.assertEqual(
                observation.request.request_id,
                "req.003",
            )

    def test_arbitrary_order_can_change_sequence_without_changing_values(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        self.assertNotEqual(
            sequence_a,
            sequence_b,
        )

        self.assertEqual(
            {item.decision for item in sequence_a},
            {item.decision for item in sequence_b},
        )

    def test_arbitrary_order_does_not_justify_first_as_semantically_first(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [accepted, rejected]

        ordering_basis = "arbitrary"

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

        # The first element is first in the representation,
        # but there is no evidence that it is semantically first.
        self.assertNotEqual(
            ordering_basis,
            "semantic",
        )

    def test_arbitrary_order_does_not_justify_last_as_semantically_last(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [rejected, accepted]

        ordering_basis = "arbitrary"

        self.assertEqual(
            sequence[-1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

        self.assertNotEqual(
            ordering_basis,
            "semantic",
        )

    def test_arbitrary_order_does_not_establish_transition(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [rejected, accepted]

        ordering_basis = "arbitrary"

        transition = (
            sequence[0].decision,
            sequence[1].decision,
        )

        self.assertEqual(
            transition,
            (
                ExperimentalAdmissionDecision.REJECTED,
                ExperimentalAdmissionDecision.ACCEPTED,
            ),
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

    def test_reverse_arbitrary_order_produces_different_representation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        ordering_basis_a = "arbitrary"
        ordering_basis_b = "arbitrary"

        self.assertNotEqual(
            sequence_a,
            sequence_b,
        )

        self.assertEqual(
            ordering_basis_a,
            ordering_basis_b,
        )

    def test_arbitrary_order_preserves_observation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        self.assertIs(
            sequence_a[0],
            rejected,
        )

        self.assertIs(
            sequence_a[1],
            accepted,
        )

        self.assertIs(
            sequence_b[0],
            accepted,
        )

        self.assertIs(
            sequence_b[1],
            rejected,
        )

    def test_arbitrary_order_can_be_discarded_without_losing_values(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
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

        unordered_values = {
            observation.decision
            for observation in sequence
        }

        self.assertEqual(
            unordered_values,
            {
                ExperimentalAdmissionDecision.REJECTED,
                ExperimentalAdmissionDecision.ACCEPTED,
            },
        )

    def test_arbitrary_order_is_distinct_from_semantic_ordering(self):
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

        ordering_basis = "arbitrary"

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

        self.assertNotEqual(
            ordering_basis,
            "semantic",
        )

    def test_minimal_model_does_not_require_semantic_order_for_arbitrary_collection(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
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

        ordering_basis = "arbitrary"

        self.assertEqual(
            len(sequence),
            2,
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )


if __name__ == "__main__":
    unittest.main()