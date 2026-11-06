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
class ExperimentalAuthorityConflict:
    scope: str
    authority_a: ExperimentalOrderingAuthority
    authority_b: ExperimentalOrderingAuthority


class TestAdmissionDecisionOrderingAuthorityConflictResolutionOwnership(
    unittest.TestCase
):

    def test_observation_does_not_own_resolution(self):
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

        self.assertNotIn(
            "resolution",
            observation.__dict__,
        )

    def test_conflict_can_exist_independently_of_observation_resolution(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertNotEqual(
            conflict.authority_a.authority_id,
            conflict.authority_b.authority_id,
        )

    def test_context_can_supply_resolution_policy(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "resolution_policy": "prefer-authority-a",
        }

        self.assertEqual(
            context["resolution_policy"],
            "prefer-authority-a",
        )

    def test_resolution_policy_does_not_mutate_conflict(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        before = conflict

        context = {
            "conflict": conflict,
            "resolution_policy": "prefer-authority-b",
        }

        self.assertIs(
            before,
            context["conflict"],
        )

    def test_resolution_policy_does_not_mutate_observation(self):
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

        before = observation

        context = {
            "observation": observation,
            "resolution_policy": "prefer-authority-a",
        }

        self.assertIs(
            before,
            context["observation"],
        )

    def test_resolution_can_be_external_to_authorities(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "resolution_policy": "external-policy",
        }

        self.assertEqual(
            context["resolution_policy"],
            "external-policy",
        )

    def test_resolution_can_depend_on_scope(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "scope": conflict.scope,
            "conflict": conflict,
            "resolution_policy": "scope-policy",
        }

        self.assertEqual(
            context["scope"],
            "scope-a",
        )

    def test_resolution_does_not_change_decision_value(self):
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

        context = {
            "observation": observation,
            "resolution_policy": "prefer-authority-b",
        }

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_resolution_does_not_change_request_identity(self):
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

        context = {
            "observation": observation,
            "resolution_policy": "prefer-authority-a",
        }

        self.assertEqual(
            context["observation"].request.request_id,
            "req.004",
        )

    def test_resolution_can_produce_contextual_outcome(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "resolution_policy": "prefer-authority-a",
        }

        resolution = {
            "selected_authority":
                context["conflict"].authority_a.authority_id
        }

        self.assertEqual(
            resolution["selected_authority"],
            "authority-a",
        )

    def test_resolution_outcome_can_remain_outside_observation(self):
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

        resolution = {
            "selected_authority": "authority-a",
        }

        self.assertNotIn(
            "selected_authority",
            observation.__dict__,
        )

    def test_minimal_model_can_resolve_without_resolution_object(self):
        context = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "resolution_policy": "prefer-authority-a",
        }

        selected_authority = (
            context["authority_a"]
            if context["resolution_policy"] == "prefer-authority-a"
            else context["authority_b"]
        )

        self.assertEqual(
            selected_authority,
            "authority-a",
        )


if __name__ == "__main__":
    unittest.main()