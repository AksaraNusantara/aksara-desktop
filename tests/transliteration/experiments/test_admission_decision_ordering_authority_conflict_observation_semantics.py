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


class TestAdmissionDecisionOrderingAuthorityConflictObservationSemantics(
    unittest.TestCase
):

    def test_conflict_does_not_change_observation_identity(self):
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

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].observation_id,
            "obs.001",
        )

    def test_conflict_does_not_change_decision_value(self):
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

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_conflict_does_not_change_request_identity(self):
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

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].request.request_id,
            "req.003",
        )

    def test_conflict_does_not_mutate_observation(self):
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

        before = observation

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        _ = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertIs(
            before,
            observation,
        )

    def test_conflict_does_not_require_new_observation(self):
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

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertIs(
            context["observation"],
            observation,
        )

    def test_same_observation_can_be_seen_before_and_after_conflict(self):
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

        before = observation

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        after = observation

        self.assertIs(before, after)
        self.assertIs(after, observation)

    def test_conflict_is_external_to_observation_state(self):
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

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        self.assertNotIn(
            "conflict",
            observation.__dict__,
        )

        self.assertEqual(
            conflict.scope,
            "scope-a",
        )

    def test_conflict_can_exist_without_changing_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.008",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        self.assertEqual(
            observation.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            conflict.authority_a.authority_id,
            conflict.authority_b.authority_id,
        )

    def test_multiple_conflicts_can_reference_same_observation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.009",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        conflict_a = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        conflict_b = ExperimentalAuthorityConflict(
            scope="scope-b",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-c"),
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

    def test_conflict_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.010",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context = {
            "conflict": conflict,
            "observation": observation,
        }

        self.assertEqual(
            context["observation"].request.operation.operation_id,
            "op.transliterate",
        )

    def test_minimal_observation_contains_no_conflict_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.011",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            set(observation.__dict__.keys()),
            {"observation_id", "request", "decision"},
        )

    def test_conflict_can_be_removed_without_destroying_observation_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observation = ExperimentalAdmissionDecisionObservation(
            observation_id="obs.012",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority("authority-a"),
            authority_b=ExperimentalOrderingAuthority("authority-b"),
        )

        context_with_conflict = {
            "conflict": conflict,
            "observation": observation,
        }

        context_without_conflict = {
            "observation": observation,
        }

        self.assertEqual(
            context_with_conflict["observation"].observation_id,
            context_without_conflict["observation"].observation_id,
        )

        self.assertEqual(
            context_with_conflict["observation"].decision,
            context_without_conflict["observation"].decision,
        )


if __name__ == "__main__":
    unittest.main()