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


class TestAdmissionDecisionOrderingAuthorityOwnership(unittest.TestCase):

    def test_observation_can_exist_without_ordering_authority(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        ordering_authority = None

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(
            ordering_authority,
        )

    def test_ordering_can_be_external_to_observation(self):
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

        ordering_basis = "external-observation-order"

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
            "external-observation-order",
        )

    def test_observation_identity_does_not_define_ordering_authority(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        ordering_authority = "external-context"

        self.assertEqual(
            observation.request.request_id,
            "req.003",
        )

        self.assertEqual(
            ordering_authority,
            "external-context",
        )

    def test_same_observation_can_participate_in_different_ordering_contexts(self):
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

    def test_ordering_authority_can_be_represented_without_mutating_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        original = observation

        ordering_context = {
            "authority": "external-context",
            "observation": observation,
        }

        self.assertIs(
            ordering_context["observation"],
            original,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_authority_is_distinct_from_decision_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        authority = "execution-context"

        self.assertNotEqual(
            authority,
            observation.decision,
        )

    def test_authority_is_distinct_from_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        authority = "execution-context"

        self.assertNotEqual(
            authority,
            request.request_id,
        )

    def test_authority_is_distinct_from_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        authority = "execution-context"

        self.assertNotEqual(
            authority,
            operation.operation_id,
        )

    def test_ordering_can_be_meaningful_without_being_intrinsic_to_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
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

    def test_removing_authority_context_does_not_destroy_observation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority = "external-context"

        self.assertEqual(
            observation.request.request_id,
            "req.010",
        )

        authority = None

        self.assertEqual(
            observation.request.request_id,
            "req.010",
        )

        self.assertIsNone(
            authority,
        )

    def test_authority_context_can_be_changed_without_mutating_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        authority_a = "context-a"
        authority_b = "context-b"

        self.assertNotEqual(
            authority_a,
            authority_b,
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_minimal_model_does_not_require_authority_field_on_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        observation_fields = {
            "request": observation.request,
            "decision": observation.decision,
        }

        self.assertEqual(
            set(observation_fields.keys()),
            {
                "request",
                "decision",
            },
        )

        self.assertNotIn(
            "ordering_authority",
            observation_fields,
        )


if __name__ == "__main__":
    unittest.main()