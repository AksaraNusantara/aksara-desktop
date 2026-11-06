import unittest
from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime


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


@dataclass(frozen=True)
class ExperimentalTemporalObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision
    timestamp: datetime


class TestAdmissionDecisionTemporalMetadata(unittest.TestCase):

    def test_ordering_exists_without_timestamp(self):
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

    def test_ordering_without_timestamp_preserves_request_identity(self):
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

        for observation in sequence:
            self.assertEqual(
                observation.request.request_id,
                "req.002",
            )

    def test_ordering_without_timestamp_preserves_first_and_last(self):
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

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[-1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_timestamp_can_be_added_without_defining_ordering_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp_a = datetime(
            2026, 1, 1, 10, 0, 0
        )

        timestamp_b = datetime(
            2026, 1, 1, 10, 1, 0
        )

        sequence = [
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
                timestamp=timestamp_a,
            ),
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
                timestamp=timestamp_b,
            ),
        ]

        self.assertEqual(
            sequence[0].timestamp,
            timestamp_a,
        )

        self.assertEqual(
            sequence[1].timestamp,
            timestamp_b,
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_ordering_and_timestamp_are_distinguishable_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp_a = datetime(
            2026, 1, 1, 10, 0, 0
        )

        timestamp_b = datetime(
            2026, 1, 1, 10, 1, 0
        )

        sequence = [
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
                timestamp=timestamp_a,
            ),
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
                timestamp=timestamp_b,
            ),
        ]

        self.assertEqual(
            sequence[0].timestamp,
            timestamp_a,
        )

        self.assertEqual(
            sequence[1].timestamp,
            timestamp_b,
        )

        self.assertNotEqual(
            sequence[0].decision,
            sequence[1].decision,
        )

    def test_same_timestamp_can_still_have_ordered_positions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp = datetime(
            2026, 1, 1, 10, 0, 0
        )

        sequence = [
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
                timestamp=timestamp,
            ),
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
                timestamp=timestamp,
            ),
        ]

        self.assertEqual(
            sequence[0].timestamp,
            sequence[1].timestamp,
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_same_timestamp_does_not_collapse_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp = datetime(
            2026, 1, 1, 10, 0, 0
        )

        first = ExperimentalTemporalObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
            timestamp=timestamp,
        )

        second = ExperimentalTemporalObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
            timestamp=timestamp,
        )

        self.assertNotEqual(
            first,
            second,
        )

    def test_reordering_does_not_require_timestamp_change(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp = datetime(
            2026, 1, 1, 10, 0, 0
        )

        sequence = [
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
                timestamp=timestamp,
            ),
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
                timestamp=timestamp,
            ),
        ]

        reordered = list(reversed(sequence))

        self.assertEqual(
            reordered[0].timestamp,
            timestamp,
        )

        self.assertEqual(
            reordered[1].timestamp,
            timestamp,
        )

    def test_timestamp_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp = datetime(
            2026, 1, 1, 10, 0, 0
        )

        observation = ExperimentalTemporalObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
            timestamp=timestamp,
        )

        self.assertEqual(
            observation.request.request_id,
            "req.009",
        )

    def test_ordering_can_be_observed_when_timestamps_are_absent(self):
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
        ]

        self.assertIsInstance(
            sequence,
            list,
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_timestamp_order_and_collection_order_can_be_compared(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        timestamp_a = datetime(
            2026, 1, 1, 10, 0, 0
        )

        timestamp_b = datetime(
            2026, 1, 1, 10, 1, 0
        )

        sequence = [
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
                timestamp=timestamp_a,
            ),
            ExperimentalTemporalObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
                timestamp=timestamp_b,
            ),
        ]

        self.assertEqual(
            sequence[0].timestamp < sequence[1].timestamp,
            True,
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_minimal_ordering_model_does_not_require_temporal_metadata(self):
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
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(
            len(sequence),
            3,
        )

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            sequence[2].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[0].request.request_id,
            "req.012",
        )

        self.assertEqual(
            sequence[1].request.request_id,
            "req.012",
        )

        self.assertEqual(
            sequence[2].request.request_id,
            "req.012",
        )


if __name__ == "__main__":
    unittest.main()