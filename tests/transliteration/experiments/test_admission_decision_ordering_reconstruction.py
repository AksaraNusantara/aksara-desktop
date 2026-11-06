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


class TestAdmissionDecisionOrderingReconstruction(unittest.TestCase):

    def test_order_can_be_reconstructed_from_order_preserving_copy(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = list(original)

        self.assertEqual(
            original,
            reconstructed,
        )

    def test_reconstructed_sequence_preserves_relative_order(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = [
            original[0],
            original[1],
        ]

        self.assertEqual(
            reconstructed[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            reconstructed[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_tuple_reconstruction_preserves_ordering_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = tuple(original)

        self.assertEqual(
            reconstructed[0].decision,
            original[0].decision,
        )

        self.assertEqual(
            reconstructed[1].decision,
            original[1].decision,
        )

    def test_ordering_can_be_reconstructed_from_explicit_positions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        indexed = [
            (
                0,
                ExperimentalAdmissionDecisionObservation(
                    request=request,
                    decision=ExperimentalAdmissionDecision.REJECTED,
                ),
            ),
            (
                1,
                ExperimentalAdmissionDecisionObservation(
                    request=request,
                    decision=ExperimentalAdmissionDecision.ACCEPTED,
                ),
            ),
        ]

        reconstructed = [
            observation
            for _, observation in sorted(
                indexed,
                key=lambda item: item[0],
            )
        ]

        self.assertEqual(
            reconstructed[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            reconstructed[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_explicit_positions_can_reconstruct_original_order_after_shuffle(self):
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

        shuffled = [
            (1, accepted),
            (0, rejected),
        ]

        reconstructed = [
            observation
            for _, observation in sorted(
                shuffled,
                key=lambda item: item[0],
            )
        ]

        self.assertEqual(
            reconstructed,
            [rejected, accepted],
        )

    def test_removing_positions_can_destroy_reconstructability(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        unordered = {
            observation.decision
            for observation in original
        }

        possible_orders = {
            (
                ExperimentalAdmissionDecision.REJECTED,
                ExperimentalAdmissionDecision.ACCEPTED,
            ),
            (
                ExperimentalAdmissionDecision.ACCEPTED,
                ExperimentalAdmissionDecision.REJECTED,
            ),
        }

        self.assertEqual(
            unordered,
            {
                ExperimentalAdmissionDecision.REJECTED,
                ExperimentalAdmissionDecision.ACCEPTED,
            },
        )

        self.assertEqual(
            len(possible_orders),
            2,
        )

    def test_membership_alone_cannot_uniquely_reconstruct_order(self):
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

        unordered = {rejected, accepted}

        candidate_a = [rejected, accepted]
        candidate_b = [accepted, rejected]

        self.assertEqual(
            set(candidate_a),
            unordered,
        )

        self.assertEqual(
            set(candidate_b),
            unordered,
        )

        self.assertNotEqual(
            candidate_a,
            candidate_b,
        )

    def test_reconstruction_requires_preserved_relative_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        preserved_information = [
            (0, original[0]),
            (1, original[1]),
        ]

        self.assertEqual(
            preserved_information[0][0],
            0,
        )

        self.assertEqual(
            preserved_information[1][0],
            1,
        )

    def test_reconstruction_does_not_require_timestamp_when_position_is_preserved(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        indexed = [
            (
                0,
                ExperimentalAdmissionDecisionObservation(
                    request=request,
                    decision=ExperimentalAdmissionDecision.REJECTED,
                ),
            ),
            (
                1,
                ExperimentalAdmissionDecisionObservation(
                    request=request,
                    decision=ExperimentalAdmissionDecision.ACCEPTED,
                ),
            ),
        ]

        timestamps = None

        reconstructed = [
            observation
            for _, observation in sorted(
                indexed,
                key=lambda item: item[0],
            )
        ]

        self.assertEqual(
            reconstructed[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            reconstructed[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            timestamps,
        )

    def test_reconstruction_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = list(original)

        for observation in reconstructed:
            self.assertEqual(
                observation.request.request_id,
                "req.010",
            )

    def test_lossless_reconstruction_preserves_first_and_last(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = list(original)

        self.assertEqual(
            reconstructed[0].decision,
            original[0].decision,
        )

        self.assertEqual(
            reconstructed[-1].decision,
            original[-1].decision,
        )

    def test_minimal_reconstruction_does_not_require_ordering_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        original = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        reconstructed = list(original)

        explicit_ordering_object = None

        self.assertEqual(
            reconstructed[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            reconstructed[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            explicit_ordering_object,
        )


if __name__ == "__main__":
    unittest.main()