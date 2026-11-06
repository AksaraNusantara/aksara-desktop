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
    observation_id: str
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


@dataclass(frozen=True)
class ExperimentalOrderingAuthority:
    authority_id: str


@dataclass(frozen=True)
class ExperimentalOrderingContext:
    context_id: str
    authority: ExperimentalOrderingAuthority
    observations: tuple


class TestAdmissionDecisionOrderingAuthorityConflict(unittest.TestCase):

    def test_different_authorities_are_not_automatically_a_conflict(self):
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

    def test_same_observation_can_exist_in_two_non_conflicting_contexts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            authority=authority_a,
            observations=(observation,),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            authority=authority_b,
            observations=(observation,),
        )

        self.assertIn(
            observation,
            context_a.observations,
        )

        self.assertIn(
            observation,
            context_b.observations,
        )

    def test_authority_conflict_requires_same_semantic_scope(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="scope-a",
            authority=authority_a,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="scope-b",
            authority=authority_b,
            observations=(),
        )

        self.assertNotEqual(
            context_a.context_id,
            context_b.context_id,
        )

    def test_different_scope_prevents_automatic_conflict(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="scope-a",
            authority=authority_a,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="scope-b",
            authority=authority_b,
            observations=(),
        )

        self.assertNotEqual(
            context_a.context_id,
            context_b.context_id,
        )

    def test_same_scope_can_expose_authority_conflict(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="same-scope",
            authority=authority_a,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="same-scope",
            authority=authority_b,
            observations=(),
        )

        self.assertEqual(
            context_a.context_id,
            context_b.context_id,
        )

        self.assertNotEqual(
            context_a.authority.authority_id,
            context_b.authority.authority_id,
        )

    def test_conflict_does_not_change_observation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.002",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.observation_id,
            "obs.002",
        )

    def test_conflict_does_not_change_decision_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.003",
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
            "scope": "same-scope",
            "authority": authority_a,
            "observation": observation,
        }

        context_b = {
            "scope": "same-scope",
            "authority": authority_b,
            "observation": observation,
        }

        self.assertEqual(
            context_a["observation"].decision,
            context_b["observation"].decision,
        )

    def test_conflict_is_relationship_between_authorities_and_scope(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="same-scope",
            authority=authority_a,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="same-scope",
            authority=authority_b,
            observations=(),
        )

        conflict = (
            context_a.context_id == context_b.context_id
            and
            context_a.authority.authority_id
            != context_b.authority.authority_id
        )

        self.assertTrue(conflict)

    def test_authority_conflict_does_not_require_authority_mutation(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        self.assertEqual(
            authority_a.authority_id,
            "authority-a",
        )

        self.assertEqual(
            authority_b.authority_id,
            "authority-b",
        )

    def test_authority_conflict_does_not_require_observation_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        before = observation

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        _ = {
            "scope": "same-scope",
            "authority": authority_a,
            "observation": observation,
        }

        _ = {
            "scope": "same-scope",
            "authority": authority_b,
            "observation": observation,
        }

        self.assertIs(
            before,
            observation,
        )

    def test_minimal_observation_does_not_need_conflict_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.005",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotIn(
            "authority",
            observation.__dict__,
        )

        self.assertNotIn(
            "conflict",
            observation.__dict__,
        )

    def test_conflict_can_be_detected_without_changing_observation_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.006",
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
            "scope": "same-scope",
            "authority": authority_a,
            "observation": observation,
        }

        context_b = {
            "scope": "same-scope",
            "authority": authority_b,
            "observation": observation,
        }

        conflict = (
            context_a["scope"] == context_b["scope"]
            and
            context_a["authority"].authority_id
            != context_b["authority"].authority_id
        )

        self.assertTrue(conflict)

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )


if __name__ == "__main__":
    unittest.main()