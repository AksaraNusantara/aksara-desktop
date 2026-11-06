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


class TestAdmissionDecisionOrderingAuthority(unittest.TestCase):

    def test_ordered_collection_can_represent_a_sequence(self):
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

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_collection_order_exists_without_explicit_order_metadata(self):
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
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_same_observations_can_be_presented_in_different_orders(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
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

    def test_order_changes_position_but_not_observation_identity(self):
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

        self.assertIs(
            sequence_a[0],
            rejected,
        )

        self.assertIs(
            sequence_b[1],
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

    def test_request_identity_is_independent_of_collection_order(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
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

        for observation in sequence_a:
            self.assertEqual(
                observation.request.request_id,
                "req.005",
            )

        for observation in sequence_b:
            self.assertEqual(
                observation.request.request_id,
                "req.005",
            )

    def test_order_alone_does_not_explain_why_the_order_exists(self):
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

        ordering_basis = None

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(ordering_basis)

    def test_ordered_collection_can_preserve_an_existing_ordering_basis(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        ordering_basis = "experimental-observation-order"

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

        self.assertEqual(
            ordering_basis,
            "experimental-observation-order",
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_ordering_basis_is_distinct_from_decision_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
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

        ordering_basis = "experimental-observation-order"

        self.assertNotEqual(
            ordering_basis,
            sequence[0].decision,
        )

        self.assertNotEqual(
            ordering_basis,
            sequence[1].decision,
        )

    def test_reordering_preserves_observation_set(self):
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

        sequence = [rejected, accepted]
        reordered = [accepted, rejected]

        self.assertEqual(
            {id(observation) for observation in sequence},
            {id(observation) for observation in reordered},
        )

    def test_ordering_can_be_removed_without_destroying_observation_values(self):
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

    def test_ordering_information_is_distinct_from_membership_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
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

        ordered = [rejected, accepted]
        unordered = {rejected, accepted}

        self.assertEqual(
            len(ordered),
            len(unordered),
        )

        self.assertIn(
            rejected,
            unordered,
        )

        self.assertIn(
            accepted,
            unordered,
        )

    def test_minimal_model_does_not_require_explicit_ordering_object(self):
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

        explicit_ordering_object = None

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            explicit_ordering_object,
        )


if __name__ == "__main__":
    unittest.main()