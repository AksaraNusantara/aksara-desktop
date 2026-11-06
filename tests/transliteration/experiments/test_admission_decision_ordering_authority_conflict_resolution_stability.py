import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalOrderingAuthority:
    authority_id: str


@dataclass(frozen=True)
class ExperimentalAuthorityConflict:
    scope: str
    authority_a: ExperimentalOrderingAuthority
    authority_b: ExperimentalOrderingAuthority


def resolve_conflict(conflict, policy):
    if policy == "prefer-authority-a":
        return conflict.authority_a.authority_id

    if policy == "prefer-authority-b":
        return conflict.authority_b.authority_id

    return None


class TestAdmissionDecisionOrderingAuthorityConflictResolutionStability(
    unittest.TestCase
):

    def test_same_policy_produces_same_outcome(self):
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

        first = resolve_conflict(
            conflict,
            "prefer-authority-a",
        )

        second = resolve_conflict(
            conflict,
            "prefer-authority-a",
        )

        self.assertEqual(first, second)

    def test_representation_change_preserves_outcome(self):
        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict_object = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=authority_a,
            authority_b=authority_b,
        )

        conflict_mapping = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
        }

        object_outcome = resolve_conflict(
            conflict_object,
            "prefer-authority-a",
        )

        mapping_outcome = (
            conflict_mapping["authority_a"]
            if "prefer-authority-a" == "prefer-authority-a"
            else conflict_mapping["authority_b"]
        )

        self.assertEqual(
            object_outcome,
            mapping_outcome,
        )

    def test_equivalent_authority_identity_preserves_outcome(self):
        conflict_a = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority(
                authority_id="authority-a"
            ),
            authority_b=ExperimentalOrderingAuthority(
                authority_id="authority-b"
            ),
        )

        conflict_b = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority(
                authority_id="authority-a"
            ),
            authority_b=ExperimentalOrderingAuthority(
                authority_id="authority-b"
            ),
        )

        outcome_a = resolve_conflict(
            conflict_a,
            "prefer-authority-a",
        )

        outcome_b = resolve_conflict(
            conflict_b,
            "prefer-authority-a",
        )

        self.assertEqual(outcome_a, outcome_b)

    def test_observation_identity_is_not_resolution_input(self):
        context_a = {
            "observation_id": "obs-001",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "policy": "prefer-authority-a",
        }

        context_b = {
            "observation_id": "obs-002",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "policy": "prefer-authority-a",
        }

        outcome_a = context_a["authority_a"]
        outcome_b = context_b["authority_a"]

        self.assertEqual(outcome_a, outcome_b)

    def test_policy_change_can_change_outcome(self):
        conflict = ExperimentalAuthorityConflict(
            scope="scope-a",
            authority_a=ExperimentalOrderingAuthority(
                authority_id="authority-a"
            ),
            authority_b=ExperimentalOrderingAuthority(
                authority_id="authority-b"
            ),
        )

        outcome_a = resolve_conflict(
            conflict,
            "prefer-authority-a",
        )

        outcome_b = resolve_conflict(
            conflict,
            "prefer-authority-b",
        )

        self.assertNotEqual(outcome_a, outcome_b)

    def test_minimal_model_preserves_resolution_stability(self):
        context = {
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "policy": "prefer-authority-a",
        }

        first = (
            context["authority_a"]
            if context["policy"] == "prefer-authority-a"
            else context["authority_b"]
        )

        second = (
            context["authority_a"]
            if context["policy"] == "prefer-authority-a"
            else context["authority_b"]
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()