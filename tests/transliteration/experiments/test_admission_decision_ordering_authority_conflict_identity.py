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
    conflict_id: str
    scope: str
    authority_a: ExperimentalOrderingAuthority
    authority_b: ExperimentalOrderingAuthority


class TestAdmissionDecisionOrderingAuthorityConflictIdentity(unittest.TestCase):

    def test_conflict_can_have_independent_identity(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-001",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertEqual(
            conflict.conflict_id,
            "conflict-001",
        )

    def test_two_conflicts_can_have_distinct_identity(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict_a = ExperimentalAuthorityConflict(
            conflict_id="conflict-a",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        conflict_b = ExperimentalAuthorityConflict(
            conflict_id="conflict-b",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertNotEqual(
            conflict_a.conflict_id,
            conflict_b.conflict_id,
        )

    def test_conflict_identity_is_distinct_from_authority_identity(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-001",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertNotEqual(
            conflict.conflict_id,
            authority_a.authority_id,
        )

        self.assertNotEqual(
            conflict.conflict_id,
            authority_b.authority_id,
        )

    def test_conflict_can_reference_two_distinct_authorities(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-002",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertNotEqual(
            conflict.authority_a.authority_id,
            conflict.authority_b.authority_id,
        )

    def test_conflict_scope_is_distinct_from_conflict_identity(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-003",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertNotEqual(
            conflict.conflict_id,
            conflict.scope,
        )

    def test_conflict_can_be_associated_with_observation_without_becoming_observation_property(self):
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

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-004",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertIs(
            context["observation"],
            observation,
        )

        self.assertIs(
            context["conflict"],
            conflict,
        )

        self.assertNotIn(
            "conflict",
            observation.__dict__,
        )

    def test_same_observation_can_be_associated_with_multiple_conflicts(self):
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

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        authority_c = ExperimentalOrderingAuthority(
            authority_id="authority-c"
        )

        conflict_a = ExperimentalAuthorityConflict(
            conflict_id="conflict-a",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        conflict_b = ExperimentalAuthorityConflict(
            conflict_id="conflict-b",
            scope="scope-b",
            authority_a=authority_a,
            authority_b=authority_c,
        )

        context_a = {
            "conflict": conflict_a,
            "observation": observation,
        }

        context_b = {
            "conflict": conflict_b,
            "observation": observation,
        }

        self.assertIs(
            context_a["observation"],
            context_b["observation"],
        )

        self.assertNotEqual(
            context_a["conflict"].conflict_id,
            context_b["conflict"].conflict_id,
        )

    def test_conflict_identity_does_not_change_decision_value(self):
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

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-005",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_conflict_identity_does_not_change_request_identity(self):
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

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-006",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].request.request_id,
            "req.004",
        )

    def test_conflict_can_be_detected_without_mutating_observation(self):
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

        before = observation

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-007",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        _ = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertIs(
            before,
            observation,
        )

    def test_minimal_observation_does_not_require_conflict_identity(self):
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

        self.assertNotIn(
            "conflict_id",
            observation.__dict__,
        )

    def test_conflict_identity_can_exist_without_execution(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            conflict_id="conflict-008",
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertEqual(
            conflict.conflict_id,
            "conflict-008",
        )

    def test_minimal_context_can_represent_conflict_without_explicit_conflict_object(self):
        context = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
        }

        conflict = (
            context["scope"] == "scope-a"
            and context["authority_a"] != context["authority_b"]
        )

        self.assertTrue(conflict)


if __name__ == "__main__":
    unittest.main()