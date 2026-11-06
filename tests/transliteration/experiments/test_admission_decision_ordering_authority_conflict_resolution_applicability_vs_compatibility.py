import unittest


def evaluate_compatibility(
    required_authority,
    selected_authority,
):
    return required_authority == selected_authority


def evaluate_applicability(
    scope,
    resolution,
):
    return (
        resolution["allowed_scope"] == scope
    )


class TestAdmissionDecisionOrderingAuthorityConflictResolutionApplicabilityVsCompatibility(
    unittest.TestCase
):

    def test_compatible_and_applicable_can_both_be_true(self):
        compatibility = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(compatibility)
        self.assertTrue(applicability)

    def test_compatible_can_be_true_while_applicability_is_false(
        self,
    ):
        compatibility = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-b",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(compatibility)
        self.assertFalse(applicability)

    def test_applicability_can_be_true_while_compatibility_is_false(
        self,
    ):
        compatibility = evaluate_compatibility(
            required_authority="authority-b",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertFalse(compatibility)
        self.assertTrue(applicability)

    def test_compatibility_uses_semantic_requirements(self):
        result = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        self.assertTrue(result)

    def test_applicability_uses_scope_context(self):
        result = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(result)

    def test_changing_authority_can_change_compatibility_only(
        self,
    ):
        compatibility_a = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        compatibility_b = evaluate_compatibility(
            required_authority="authority-b",
            selected_authority="authority-a",
        )

        applicability_a = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        applicability_b = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(compatibility_a)
        self.assertFalse(compatibility_b)
        self.assertEqual(
            applicability_a,
            applicability_b,
        )

    def test_changing_scope_can_change_applicability_only(
        self,
    ):
        applicability_a = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        applicability_b = evaluate_applicability(
            scope="scope-b",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        compatibility_a = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        compatibility_b = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        self.assertTrue(applicability_a)
        self.assertFalse(applicability_b)
        self.assertEqual(
            compatibility_a,
            compatibility_b,
        )

    def test_same_resolution_can_have_different_applicability(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        result_a = evaluate_applicability(
            scope="scope-a",
            resolution=resolution,
        )

        result_b = evaluate_applicability(
            scope="scope-b",
            resolution=resolution,
        )

        self.assertTrue(result_a)
        self.assertFalse(result_b)

    def test_same_scope_can_have_different_compatibility(self):
        scope = "scope-a"

        applicability = evaluate_applicability(
            scope=scope,
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        compatibility_a = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        compatibility_b = evaluate_compatibility(
            required_authority="authority-b",
            selected_authority="authority-a",
        )

        self.assertTrue(applicability)
        self.assertTrue(compatibility_a)
        self.assertFalse(compatibility_b)

    def test_compatibility_and_applicability_have_different_inputs(
        self,
    ):
        compatibility = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(compatibility)
        self.assertTrue(applicability)

    def test_combined_evaluation_preserves_both_semantics(self):
        compatibility = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-a",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        combined = {
            "compatible": compatibility,
            "applicable": applicability,
        }

        self.assertTrue(combined["compatible"])
        self.assertTrue(combined["applicable"])

    def test_one_semantic_result_does_not_imply_the_other(self):
        compatibility = evaluate_compatibility(
            required_authority="authority-a",
            selected_authority="authority-a",
        )

        applicability = evaluate_applicability(
            scope="scope-b",
            resolution={
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(compatibility)
        self.assertFalse(applicability)

    def test_minimal_model_preserves_distinction(self):
        compatibility = (
            "authority-a" == "authority-a"
        )

        applicability = (
            "scope-a" == "scope-b"
        )

        self.assertTrue(compatibility)
        self.assertFalse(applicability)


if __name__ == "__main__":
    unittest.main()