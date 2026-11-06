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


class TestAdmissionDecisionOrderingVsRequest(unittest.TestCase):

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

    def test_all_observations_reference_same_request(self):
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

        self.assertIs(
            sequence[0].request,
            sequence[1].request,
        )

    def test_reordering_does_not_create_new_request(self):
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

        reordered = list(reversed(sequence))

        self.assertIs(
            reordered[0].request,
            request,
        )

        self.assertIs(
            reordered[1].request,
            request,
        )

    def test_request_id_is_independent_of_observation_position(self):
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

        self.assertEqual(
            request.request_id,
            "req.004",
        )

        self.assertEqual(
            reordered[0].request.request_id,
            "req.004",
        )

        self.assertEqual(
            reordered[1].request.request_id,
            "req.004",
        )

    def test_different_request_id_means_different_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_a = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        request_b = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertNotEqual(
            request_a.request_id,
            request_b.request_id,
        )

    def test_same_request_can_have_multiple_orderings(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
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

        sequence_b = [
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
            sequence_a[0].request.request_id,
            sequence_b[0].request.request_id,
        )

        self.assertEqual(
            sequence_a[1].request.request_id,
            sequence_b[1].request.request_id,
        )

    def test_ordering_does_not_change_request_object(self):
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

        reordered = list(reversed(sequence))

        self.assertEqual(
            reordered[0].request,
            request,
        )

        self.assertEqual(
            reordered[1].request,
            request,
        )

    def test_ordering_is_not_encoded_in_request_identity(self):
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

        reordered = list(reversed(sequence))

        self.assertEqual(
            sequence[0].request.request_id,
            reordered[0].request.request_id,
        )

        self.assertEqual(
            sequence[1].request.request_id,
            reordered[1].request.request_id,
        )

    def test_request_identity_survives_multiple_decision_values(self):
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
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
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
                "req.010",
            )

    def test_reordering_does_not_require_request_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request = request

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

        self.assertIs(
            request,
            original_request,
        )

        for observation in reordered:
            self.assertIs(
                observation.request,
                original_request,
            )

    def test_ordering_and_request_identity_are_separate_concepts(self):
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

        self.assertNotEqual(
            sequence_a,
            sequence_b,
        )

        self.assertEqual(
            sequence_a[0].request.request_id,
            sequence_b[0].request.request_id,
        )

        self.assertEqual(
            sequence_a[1].request.request_id,
            sequence_b[1].request.request_id,
        )


if __name__ == "__main__":
    unittest.main()