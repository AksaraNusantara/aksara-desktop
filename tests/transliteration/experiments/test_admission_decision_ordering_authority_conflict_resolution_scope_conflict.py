import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentalScope:
    scope_id: str
    required_authority: str


@dataclass(frozen=True)
class ExperimentalResolution:
    selected_authority: str


def evaluate_compatibility(scope, resolution):
    return (
        scope.required_authority
        == resolution.selected_authority
    )


class TestAdmissionDecisionOrderingAuthorityConflictResolutionScopeConflict(
    unittest.TestCase
):

    def test_matching_scope_and_resolution_are_compatible(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertTrue(
            evaluate_compatibility(scope, resolution)
        )

    def test_different_scope_requirement_can_create_conflict(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertFalse(
            evaluate_compatibility(scope, resolution)
        )

    def test_conflict_is_not_resolution_mutation(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        before = resolution

        compatible = evaluate_compatibility(
            scope,
            resolution,
        )

        self.assertFalse(compatible)

        self.assertIs(
            before,
            resolution,
        )

    def test_conflict_does_not_change_selected_authority(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        evaluate_compatibility(
            scope,
            resolution,
        )

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

    def test_same_resolution_can_be_compatible_with_one_scope(
        self,
    ):
        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertTrue(
            evaluate_compatibility(
                scope_a,
                resolution,
            )
        )

    def test_same_resolution_can_conflict_with_another_scope(
        self,
    ):
        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertTrue(
            evaluate_compatibility(
                scope_a,
                resolution,
            )
        )

        self.assertFalse(
            evaluate_compatibility(
                scope_b,
                resolution,
            )
        )

    def test_scope_conflict_does_not_create_new_resolution(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        before = resolution

        evaluate_compatibility(
            scope,
            resolution,
        )

        self.assertIs(
            before,
            resolution,
        )

    def test_scope_conflict_can_be_observed_externally(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        conflict = {
            "scope": scope.scope_id,
            "selected_authority":
                resolution.selected_authority,
            "required_authority":
                scope.required_authority,
        }

        self.assertEqual(
            conflict["scope"],
            "scope-b",
        )

        self.assertEqual(
            conflict["selected_authority"],
            "authority-a",
        )

        self.assertEqual(
            conflict["required_authority"],
            "authority-b",
        )

    def test_conflict_is_relational(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        first = evaluate_compatibility(
            scope,
            resolution,
        )

        second = evaluate_compatibility(
            scope,
            ExperimentalResolution(
                selected_authority="authority-b"
            ),
        )

        self.assertFalse(first)
        self.assertTrue(second)

    def test_changing_scope_can_remove_conflict(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        self.assertFalse(
            evaluate_compatibility(
                scope_b,
                resolution,
            )
        )

        self.assertTrue(
            evaluate_compatibility(
                scope_a,
                resolution,
            )
        )

    def test_changing_resolution_can_remove_conflict(self):
        scope = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        resolution_a = ExperimentalResolution(
            selected_authority="authority-a"
        )

        resolution_b = ExperimentalResolution(
            selected_authority="authority-b"
        )

        self.assertFalse(
            evaluate_compatibility(
                scope,
                resolution_a,
            )
        )

        self.assertTrue(
            evaluate_compatibility(
                scope,
                resolution_b,
            )
        )

    def test_minimal_model_needs_only_scope_and_resolution(
        self,
    ):
        scope = {
            "required_authority": "authority-b"
        }

        resolution = {
            "selected_authority": "authority-a"
        }

        conflict = (
            scope["required_authority"]
            != resolution["selected_authority"]
        )

        self.assertTrue(conflict)


if __name__ == "__main__":
    unittest.main()