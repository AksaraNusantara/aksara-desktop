import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalScope:
    scope_id: str


@dataclass(frozen=True)
class ExperimentalOrderingAuthority:
    authority_id: str


@dataclass(frozen=True)
class ExperimentalAuthorityConflict:
    scope: ExperimentalScope
    authority_a: ExperimentalOrderingAuthority
    authority_b: ExperimentalOrderingAuthority


@dataclass(frozen=True)
class ExperimentalResolution:
    selected_authority: str


class TestAdmissionDecisionOrderingAuthorityConflictResolutionScopeIdentity(
    unittest.TestCase
):

    def test_scope_has_identity_distinct_from_resolution(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertNotEqual(
            scope.scope_id,
            resolution.selected_authority,
        )

    def test_conflict_can_reference_scope(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        authority_a = ExperimentalOrderingAuthority(
            authority_id="authority-a"
        )

        authority_b = ExperimentalOrderingAuthority(
            authority_id="authority-b"
        )

        conflict = ExperimentalAuthorityConflict(
            scope=scope,
            authority_a=authority_a,
            authority_b=authority_b,
        )

        self.assertEqual(
            conflict.scope.scope_id,
            "scope-a",
        )

    def test_resolution_does_not_need_scope_identity(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertFalse(
            hasattr(resolution, "scope_id")
        )

    def test_resolution_can_exist_without_scope_attribute(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

    def test_same_resolution_can_be_referenced_by_different_scopes(
        self,
    ):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context_a = {
            "scope": scope_a,
            "resolution": resolution,
        }

        context_b = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            context_a["resolution"],
            context_b["resolution"],
        )

    def test_scope_identity_does_not_change_resolution_identity(
        self,
    ):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        context_a = {
            "scope": scope_a,
            "resolution": resolution,
        }

        context_b = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            context_a["resolution"],
            context_b["resolution"],
        )

    def test_resolution_outcome_can_be_scope_independent(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution_a = ExperimentalResolution(
            selected_authority="authority-a"
        )

        resolution_b = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertEqual(
            resolution_a.selected_authority,
            resolution_b.selected_authority,
        )

        self.assertNotEqual(
            scope_a.scope_id,
            scope_b.scope_id,
        )

    def test_scope_can_change_without_mutating_resolution(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        before = resolution

        context = {
            "scope": scope_b,
            "resolution": resolution,
        }

        self.assertIs(
            before,
            context["resolution"],
        )

    def test_resolution_identity_is_not_scope_identity(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertNotEqual(
            id(scope),
            id(resolution),
        )

    def test_scope_can_exist_without_resolution(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        self.assertEqual(
            scope.scope_id,
            "scope-a",
        )

    def test_resolution_can_exist_without_conflict(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

    def test_minimal_model_keeps_scope_external_to_resolution(self):
        context = {
            "scope": "scope-a",
            "authority_a": "authority-a",
            "authority_b": "authority-b",
            "selected_authority": "authority-a",
        }

        self.assertEqual(
            context["scope"],
            "scope-a",
        )

        self.assertEqual(
            context["selected_authority"],
            "authority-a",
        )

        self.assertNotIn(
            "scope",
            {
                "selected_authority":
                    context["selected_authority"]
            },
        )


if __name__ == "__main__":
    unittest.main()