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
    scope: str
    authority: ExperimentalOrderingAuthority
    observations: tuple


class TestAdmissionDecisionOrderingAuthorityScope(unittest.TestCase):

    def test_context_can_define_scope(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(),
        )

        self.assertEqual(
            context.scope,
            "scope-a",
        )

    def test_same_authority_can_participate_in_multiple_scopes(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-shared"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="scope-b",
            authority=authority,
            observations=(),
        )

        self.assertIs(
            context_a.authority,
            context_b.authority,
        )

        self.assertNotEqual(
            context_a.scope,
            context_b.scope,
        )

    def test_same_scope_can_use_different_authorities(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="shared-scope",
            authority=authority_a,
            observations=(),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="shared-scope",
            authority=authority_b,
            observations=(),
        )

        self.assertEqual(
            context_a.scope,
            context_b.scope,
        )

        self.assertNotEqual(
            context_a.authority.authority_id,
            context_b.authority.authority_id,
        )

    def test_scope_does_not_change_observation_identity(self):
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

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(observation,),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="scope-b",
            authority=authority,
            observations=(observation,),
        )

        self.assertIs(
            context_a.observations[0],
            context_b.observations[0],
        )

    def test_scope_does_not_change_decision_value(self):
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

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(observation,),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="scope-b",
            authority=authority,
            observations=(observation,),
        )

        self.assertEqual(
            context_a.observations[0].decision,
            context_b.observations[0].decision,
        )

    def test_scope_is_distinct_from_authority_identity(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(),
        )

        self.assertNotEqual(
            context.scope,
            context.authority.authority_id,
        )

    def test_scope_is_distinct_from_context_identity(self):
        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(),
        )

        self.assertNotEqual(
            context.context_id,
            context.scope,
        )

    def test_scope_can_be_changed_without_mutating_observation(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(observation,),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="scope-b",
            authority=authority,
            observations=(observation,),
        )

        self.assertIs(
            context_a.observations[0],
            context_b.observations[0],
        )

    def test_scope_can_be_represented_without_being_observation_property(self):
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
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertNotIn(
            "scope",
            observation.__dict__,
        )

    def test_same_observation_can_participate_in_multiple_scopes(self):
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

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context_a = ExperimentalOrderingContext(
            context_id="context-a",
            scope="scope-a",
            authority=authority,
            observations=(observation,),
        )

        context_b = ExperimentalOrderingContext(
            context_id="context-b",
            scope="scope-b",
            authority=authority,
            observations=(observation,),
        )

        self.assertIs(
            context_a.observations[0],
            context_b.observations[0],
        )

        self.assertNotEqual(
            context_a.scope,
            context_b.scope,
        )

    def test_scope_difference_does_not_require_new_observation(self):
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

        authority = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        context_a = {
            "scope": "scope-a",
            "authority": authority,
            "observation": observation,
        }

        context_b = {
            "scope": "scope-b",
            "authority": authority,
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

    def test_minimal_model_can_keep_scope_outside_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.007",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        context = {
            "scope": "external-ordering-scope",
            "authority": "external-policy",
            "observation": observation,
        }

        self.assertEqual(
            context["scope"],
            "external-ordering-scope",
        )

        self.assertEqual(
            context["authority"],
            "external-policy",
        )

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )


if __name__ == "__main__":
    unittest.main()