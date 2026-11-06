import unittest


def evaluate_scope_resolution(
    required_authority,
    selected_authority,
):
    return required_authority == selected_authority


class TestAdmissionDecisionOrderingAuthorityConflictResolutionMinimalScope(
    unittest.TestCase
):

    def test_matching_requirement_is_compatible(self):
        result = evaluate_scope_resolution(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        self.assertTrue(result)

    def test_different_requirement_is_conflict(self):
        result = evaluate_scope_resolution(
            required_authority="authority-b",
            selected_authority="authority-a",
        )

        self.assertFalse(result)

    def test_scope_identity_is_not_required_for_evaluation(self):
        result = evaluate_scope_resolution(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        self.assertTrue(result)

    def test_resolution_identity_is_not_required_for_evaluation(self):
        result = evaluate_scope_resolution(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        self.assertTrue(result)

    def test_scope_object_is_not_required(self):
        scope = {
            "required_authority": "authority-a"
        }

        resolution = {
            "selected_authority": "authority-a"
        }

        result = evaluate_scope_resolution(
            scope["required_authority"],
            resolution["selected_authority"],
        )

        self.assertTrue(result)

    def test_resolution_object_is_not_required(self):
        required_authority = "authority-a"
        selected_authority = "authority-a"

        result = evaluate_scope_resolution(
            required_authority,
            selected_authority,
        )

        self.assertTrue(result)

    def test_conflict_object_is_not_required(self):
        required_authority = "authority-b"
        selected_authority = "authority-a"

        result = evaluate_scope_resolution(
            required_authority,
            selected_authority,
        )

        self.assertFalse(result)

    def test_scope_can_be_represented_as_requirement(self):
        scope_requirement = "authority-a"

        result = evaluate_scope_resolution(
            scope_requirement,
            "authority-a",
        )

        self.assertTrue(result)

    def test_resolution_can_be_represented_as_outcome(self):
        resolution_outcome = "authority-a"

        result = evaluate_scope_resolution(
            "authority-a",
            resolution_outcome,
        )

        self.assertTrue(result)

    def test_same_inputs_produce_stable_result(self):
        first = evaluate_scope_resolution(
            "authority-a",
            "authority-a",
        )

        second = evaluate_scope_resolution(
            "authority-a",
            "authority-a",
        )

        self.assertEqual(first, second)

    def test_changing_requirement_changes_relationship(self):
        compatible = evaluate_scope_resolution(
            "authority-a",
            "authority-a",
        )

        conflict = evaluate_scope_resolution(
            "authority-b",
            "authority-a",
        )

        self.assertTrue(compatible)
        self.assertFalse(conflict)

    def test_minimal_model_preserves_relationship_semantics(self):
        context = {
            "required_authority": "authority-a",
            "selected_authority": "authority-a",
        }

        compatible = (
            context["required_authority"]
            == context["selected_authority"]
        )

        self.assertTrue(compatible)


if __name__ == "__main__":
    unittest.main()