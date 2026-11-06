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


class TestAdmissionDecisionOrderingStability(unittest.TestCase):

    def test_same_order_is_stable_in_list_representation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
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
        sequence_b = [rejected, accepted]

        self.assertEqual(
            sequence_a,
            sequence_b,
        )

    def test_same_order_is_stable_when_list_is_copied(self):
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

        copied_sequence = list(sequence)

        self.assertEqual(
            sequence,
            copied_sequence,
        )

        self.assertEqual(
            sequence[0].decision,
            copied_sequence[0].decision,
        )

        self.assertEqual(
            sequence[1].decision,
            copied_sequence[1].decision,
        )

    def test_same_order_can_be_preserved_in_tuple_representation(self):
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

        list_sequence = [rejected, accepted]
        tuple_sequence = (rejected, accepted)

        self.assertEqual(
            list_sequence[0].decision,
            tuple_sequence[0].decision,
        )

        self.assertEqual(
            list_sequence[1].decision,
            tuple_sequence[1].decision,
        )

    def test_representation_type_does_not_define_ordering_value(self):
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

        list_sequence = [rejected, accepted]
        tuple_sequence = (rejected, accepted)

        self.assertNotEqual(
            type(list_sequence),
            type(tuple_sequence),
        )

        self.assertEqual(
            list_sequence[0].decision,
            tuple_sequence[0].decision,
        )

        self.assertEqual(
            list_sequence[1].decision,
            tuple_sequence[1].decision,
        )

    def test_reordering_changes_ordering_information(self):
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

        original = [rejected, accepted]
        reordered = [accepted, rejected]

        self.assertNotEqual(
            original[0].decision,
            reordered[0].decision,
        )

        self.assertNotEqual(
            original[1].decision,
            reordered[1].decision,
        )

    def test_reordering_preserves_membership_but_not_sequence(self):
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

        original = [rejected, accepted]
        reordered = [accepted, rejected]

        self.assertEqual(
            set(original),
            set(reordered),
        )

        self.assertNotEqual(
            original,
            reordered,
        )

    def test_ordering_basis_can_remain_stable_across_representation_changes(self):
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

        list_sequence = [rejected, accepted]
        tuple_sequence = (rejected, accepted)

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            list_sequence[0].decision,
            tuple_sequence[0].decision,
        )

        self.assertEqual(
            list_sequence[1].decision,
            tuple_sequence[1].decision,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

    def test_stable_order_does_not_require_same_container_type(self):
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

        representations = [
            [rejected, accepted],
            (rejected, accepted),
        ]

        self.assertEqual(
            representations[0][0].decision,
            representations[1][0].decision,
        )

        self.assertEqual(
            representations[0][1].decision,
            representations[1][1].decision,
        )

    def test_stable_order_preserves_first_and_last_positions(self):
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
        sequence_b = list(sequence_a)

        self.assertIs(
            sequence_a[0],
            sequence_b[0],
        )

        self.assertIs(
            sequence_a[-1],
            sequence_b[-1],
        )

    def test_stable_order_does_not_require_timestamp(self):
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

        timestamp_a = None
        timestamp_b = None

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            timestamp_a,
            timestamp_b,
        )

    def test_stable_order_is_distinct_from_observation_identity(self):
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

        sequence_a = [rejected, accepted]
        sequence_b = [rejected, accepted]

        self.assertIs(
            sequence_a[0],
            sequence_b[0],
        )

        self.assertIs(
            sequence_a[1],
            sequence_b[1],
        )

    def test_minimal_model_can_preserve_stable_order_without_order_object(self):
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