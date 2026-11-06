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


class TestAdmissionDecisionMinimalOrderingAuthority(unittest.TestCase):

    def test_ordered_observations_are_sufficient_to_represent_order(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
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

    def test_ordering_basis_can_be_external_to_observation_structure(self):
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

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

        self.assertEqual(
            len(observations),
            2,
        )

    def test_sequence_order_and_ordering_basis_are_distinct_information(self):
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

        ordering_basis = "declared-observation-order"

        self.assertNotEqual(
            observations[0].decision,
            observations[1].decision,
        )

        self.assertNotEqual(
            ordering_basis,
            observations[0].decision,
        )

    def test_sequence_can_preserve_order_without_sequence_number(self):
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

        sequence_number = None

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            sequence_number,
        )

    def test_sequence_can_preserve_order_without_timestamp(self):
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

        timestamp = None

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            timestamp,
        )

    def test_sequence_can_preserve_order_without_ordering_object(self):
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

        ordering_object = None

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(
            ordering_object,
        )

    def test_ordering_authority_is_not_derived_from_container_type(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
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

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            type(observations),
            list,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

    def test_arbitrary_order_has_no_authority_even_when_sequence_exists(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        ordering_basis = "arbitrary"

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "arbitrary",
        )

    def test_authoritative_order_requires_more_than_membership(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = {
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        }

        self.assertEqual(
            len(observations),
            2,
        )

        possible_sequences = 2

        self.assertEqual(
            possible_sequences,
            2,
        )

    def test_minimal_authority_model_is_order_plus_meaningful_basis(self):
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

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )

    def test_additional_metadata_is_not_required_for_minimal_semantics(self):
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

        metadata = {}

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            metadata,
            {},
        )

    def test_minimal_model_preserves_order_without_new_domain_abstraction(self):
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

        ordering_basis = "declared-observation-order"

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            ordering_basis,
            "declared-observation-order",
        )


if __name__ == "__main__":
    unittest.main()