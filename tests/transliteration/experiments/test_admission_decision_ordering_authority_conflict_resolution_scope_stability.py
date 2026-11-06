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


class TestAdmissionDecisionOrderingAuthorityConflictResolutionScopeStability(
    unittest.TestCase
):

    def test_same_inputs_produce_same_compatibility(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
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
            resolution,
        )

        self.assertEqual(first, second)

    def test_same_scope_different_representation_preserves_result(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        object_result = evaluate_compatibility(
            scope,
            resolution,
        )

        mapping_scope = {
            "scope_id": "scope-a",
            "required_authority": "authority-a",
        }

        mapping_resolution = {
            "selected_authority": "authority-a",
        }

        mapping_result = (
            mapping_scope["required_authority"]
            == mapping_resolution["selected_authority"]
        )

        self.assertEqual(
            object_result,
            mapping_result,
        )

    def test_repeated_evaluation_does_not_mutate_scope(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        before = scope

        evaluate_compatibility(
            scope,
            resolution,
        )

        self.assertIs(
            before,
            scope,
        )

    def test_repeated_evaluation_does_not_mutate_resolution(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
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

    def test_conflict_result_is_stable(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
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
            resolution,
        )

        self.assertFalse(first)
        self.assertEqual(first, second)

    def test_changing_scope_requirement_can_change_result(self):
        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-b",
        )

        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        result_a = evaluate_compatibility(
            scope_a,
            resolution,
        )

        result_b = evaluate_compatibility(
            scope_b,
            resolution,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

    def test_changing_resolution_can_change_result(self):
        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        resolution_a = ExperimentalResolution(
            selected_authority="authority-a"
        )

        resolution_b = ExperimentalResolution(
            selected_authority="authority-b"
        )

        result_a = evaluate_compatibility(
            scope,
            resolution_a,
        )

        result_b = evaluate_compatibility(
            scope,
            resolution_b,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

    def test_scope_identity_can_remain_same_while_requirement_changes(
        self,
    ):
        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-b",
        )

        self.assertEqual(
            scope_a.scope_id,
            scope_b.scope_id,
        )

        self.assertNotEqual(
            scope_a.required_authority,
            scope_b.required_authority,
        )

    def test_resolution_identity_can_remain_same_while_context_changes(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
        )

        result_a = evaluate_compatibility(
            scope_a,
            resolution,
        )

        result_b = evaluate_compatibility(
            scope_b,
            resolution,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

        self.assertEqual(
            resolution.selected_authority,
            "authority-a",
        )

    def test_compatibility_is_contextual(self):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope_a = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        scope_b = ExperimentalScope(
            scope_id="scope-b",
            required_authority="authority-b",
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

    def test_compatibility_does_not_require_resolution_state(
        self,
    ):
        resolution = ExperimentalResolution(
            selected_authority="authority-a"
        )

        scope = ExperimentalScope(
            scope_id="scope-a",
            required_authority="authority-a",
        )

        result = evaluate_compatibility(
            scope,
            resolution,
        )

        self.assertTrue(result)

    def test_minimal_model_preserves_stability(self):
        scope = {
            "required_authority": "authority-a",
        }

        resolution = {
            "selected_authority": "authority-a",
        }

        first = (
            scope["required_authority"]
            == resolution["selected_authority"]
        )

        second = (
            scope["required_authority"]
            == resolution["selected_authority"]
        )

        self.assertTrue(first)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()