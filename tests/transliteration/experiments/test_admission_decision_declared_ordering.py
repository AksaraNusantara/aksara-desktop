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


class TestAdmissionDecisionDeclaredOrdering(unittest.TestCase):

    def test_declared_ordering_can_be_represented(self):
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

        ordering_basis = "declared-observation-order"

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
            "declared-observation-order",
        )

    def test_declared_ordering_is_distinct_from_decision_value(self):
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
        ]

        ordering_basis = "declared-observation-order"

        self.assertNotEqual(
            ordering_basis,
            sequence[0].decision,
        )

        self.assertNotEqual(
            ordering_basis,
            sequence[1].decision,
        )

    def test_declared_ordering_can_distinguish_sequence_positions(self):
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

        sequence = [rejected, accepted]

        ordering_basis = "declared-observation-order"

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
            "declared-observation-order",
        )

    def test_declared_ordering_does_not_change_request_identity(self):
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

        for observation in sequence:
            self.assertEqual(
                observation.request.request_id,
                "req.004",
            )

    def test_declared_ordering_can_be_reversed_without_changing_membership(self):
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

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        self.assertNotEqual(
            sequence_a,
            sequence_b,
        )

        self.assertEqual(
            set(sequence_a),
            set(sequence_b),
        )

    def test_declared_basis_survives_sequence_reversal_as_a_declared_label(self):
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

        sequence_a = [rejected, accepted]
        sequence_b = [accepted, rejected]

        ordering_basis_a = "declared-observation-order"
        ordering_basis_b = "declared-observation-order"

        self.assertNotEqual(
            sequence_a,
            sequence_b,
        )

        self.assertEqual(
            ordering_basis_a,
            ordering_basis_b,
        )

    def test_declared_basis_does_not_itself_prove_chronology(self):
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

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

        # The declaration identifies the ordering basis,
        # but does not independently establish chronological truth.
        chronological_evidence = None

        self.assertIsNone(
            chronological_evidence,
        )

    def test_declared_basis_does_not_itself_prove_causal_transition(self):
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

        ordering_basis = "declared-observation-order"

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
            "declared-observation-order",
        )

        causal_evidence = None

        self.assertIsNone(
            causal_evidence,
        )

    def test_declared_ordering_is_more_information_than_arbitrary_ordering(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
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

        declared_basis = "declared-observation-order"
        arbitrary_basis = "arbitrary"

        self.assertNotEqual(
            declared_basis,
            arbitrary_basis,
        )

        self.assertEqual(
            len(sequence),
            2,
        )

    def test_declared_ordering_can_be_interpreted_as_ordering_information(self):
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

        ordering_basis = "declared-observation-order"

        first_position = sequence[0]
        second_position = sequence[1]

        self.assertEqual(
            first_position.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            second_position.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

    def test_declared_ordering_does_not_require_explicit_ordering_object(self):
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

        ordering_basis = "declared-observation-order"
        explicit_ordering_object = None

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
            "declared-observation-order",
        )

        self.assertIsNone(
            explicit_ordering_object,
        )

    def test_declared_ordering_does_not_require_timestamp(self):
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

        ordering_basis = "declared-observation-order"
        timestamp = None

        self.assertEqual(
            len(sequence),
            2,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

        self.assertIsNone(
            timestamp,
        )


if __name__ == "__main__":
    unittest.main()