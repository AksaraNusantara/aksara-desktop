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


@dataclass(frozen=True)
class ExperimentalOrderingAuthority:
    authority_id: str


class TestAdmissionDecisionOrderingAuthorityIdentity(unittest.TestCase):

    def test_authority_can_have_independent_identity(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        self.assertEqual(
            authority.authority_id,
            "authority-a",
        )

    def test_two_authorities_can_have_distinct_identity(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        self.assertNotEqual(
            authority_a.authority_id,
            authority_b.authority_id,
        )

    def test_authority_identity_is_distinct_from_observation_identity(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        self.assertEqual(
            observation.request.request_id,
            "req.001",
        )

        self.assertEqual(
            authority.authority_id,
            "authority-a",
        )

        self.assertNotEqual(
            observation.request.request_id,
            authority.authority_id,
        )

    def test_same_authority_can_be_associated_with_multiple_observations(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_a = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        request_b = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="carakan",
        )

        observation_a = ExperimentalAdmissionDecisionObservation(
            request=request_a,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        observation_b = ExperimentalAdmissionDecisionObservation(
            request=request_b,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-shared"
        )

        context_a = {
            "authority": authority,
            "observation": observation_a,
        }

        context_b = {
            "authority": authority,
            "observation": observation_b,
        }

        self.assertIs(
            context_a["authority"],
            context_b["authority"],
        )

        self.assertNotEqual(
            context_a["observation"].request.request_id,
            context_b["observation"].request.request_id,
        )

    def test_same_observation_can_be_associated_with_multiple_authorities(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = {
            "authority": authority_a,
            "observation": observation,
        }

        context_b = {
            "authority": authority_b,
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

        self.assertNotEqual(
            context_a["authority"].authority_id,
            context_b["authority"].authority_id,
        )

    def test_authority_identity_does_not_change_observation_identity(self):
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
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = {
            "authority": authority_a,
            "observation": observation,
        }

        context_b = {
            "authority": authority_b,
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_authority_identity_does_not_change_decision_value(self):
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

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = {
            "authority": authority_a,
            "observation": observation,
        }

        context_b = {
            "authority": authority_b,
            "observation": observation,
        }

        self.assertEqual(
            context_a["observation"].decision,
            context_b["observation"].decision,
        )

    def test_authority_identity_can_be_removed_without_changing_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context = {
            "authority": authority,
            "observation": observation,
        }

        detached_observation = context["observation"]

        self.assertIs(
            detached_observation,
            observation,
        )

        self.assertEqual(
            detached_observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_authority_identity_is_not_required_for_minimal_contextual_model(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "authority": "external-policy",
            "observation": observation,
        }

        self.assertNotIn(
            "authority_id",
            observation.__dict__,
        )

        self.assertEqual(
            context["authority"],
            "external-policy",
        )

    def test_authority_identity_can_be_shared_across_contexts(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-shared"
        )

        context_a = {
            "authority": authority,
        }

        context_b = {
            "authority": authority,
        }

        self.assertIs(
            context_a["authority"],
            context_b["authority"],
        )

    def test_distinct_authority_identity_does_not_imply_distinct_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        self.assertNotEqual(
            authority_a.authority_id,
            authority_b.authority_id,
        )

        self.assertIs(
            observation,
            observation,
        )

    def test_minimal_semantic_model_can_omit_explicit_authority_identity(self):
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

        context = {
            "authority": "ordering-context",
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].request.request_id,
            "req.010",
        )

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            context["authority"],
            "ordering-context",
        )


if __name__ == "__main__":
    unittest.main()