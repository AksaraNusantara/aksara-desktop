import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalScope:
    scope_id: str


@dataclass(frozen=True)
class ExperimentalResolution:
    selected_authority: str


class TestAdmissionDecisionOrderingAuthorityConflictResolutionApplicabilityIdentity(
    unittest.TestCase
):

    def test_resolution_has_identity_distinct_from_applicability(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            type(resolution),
            type(applicability),
        )

    def test_scope_has_identity_distinct_from_applicability(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            scope.scope_id,
            applicability["applicable"],
        )

    def test_resolution_can_exist_without_applicability(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

    def test_scope_can_exist_without_applicability(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        self.assertEqual(
            scope.scope_id,
            "scope-a",
        )

    def test_applicability_can_be_observed_without_mutating_resolution(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        before = resolution

        applicability = {
            "applicable": True,
            "resolution": resolution,
        }

        self.assertTrue(
            applicability["applicable"]
        )

        self.assertIs(
            before,
            resolution,
        )

    def test_applicability_can_be_observed_without_mutating_scope(
        self,
    ):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        before = scope

        applicability = {
            "applicable": True,
            "scope": scope,
        }

        self.assertTrue(
            applicability["applicable"]
        )

        self.assertIs(
            before,
            scope,
        )

    def test_applicability_is_not_resolution_identity(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            id(resolution),
            id(applicability),
        )

    def test_applicability_is_not_scope_identity(self):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            id(scope),
            id(applicability),
        )

    def test_applicability_can_change_with_context(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a"
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b"
        )

        applicability_a = {
            "scope": scope_a.scope_id,
            "resolution":
                resolution.selected_authority,
            "applicable": True,
        }

        applicability_b = {
            "scope": scope_b.scope_id,
            "resolution":
                resolution.selected_authority,
            "applicable": False,
        }

        self.assertNotEqual(
            applicability_a["applicable"],
            applicability_b["applicable"],
        )

    def test_resolution_identity_remains_stable_when_applicability_changes(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        first = {
            "resolution":
                resolution.selected_authority,
            "applicable": True,
        }

        second = {
            "resolution":
                resolution.selected_authority,
            "applicable": False,
        }

        self.assertEqual(
            first["resolution"],
            second["resolution"],
        )

    def test_scope_identity_remains_stable_when_applicability_changes(
        self,
    ):
        scope = ExperimentalScope(
            scope_id="scope-a"
        )

        first = {
            "scope": scope.scope_id,
            "applicable": True,
        }

        second = {
            "scope": scope.scope_id,
            "applicable": False,
        }

        self.assertEqual(
            first["scope"],
            second["scope"],
        )

    def test_applicability_does_not_require_applicability_id(self):
        applicability = {
            "applicable": True,
        }

        self.assertNotIn(
            "applicability_id",
            applicability,
        )

    def test_minimal_model_needs_no_applicability_object(self):
        scope = "scope-a"
        resolution = "authority-a"

        applicable = (
            scope == "scope-a"
            and resolution == "authority-a"
        )

        self.assertTrue(applicable)


if __name__ == "__main__":
    unittest.main()