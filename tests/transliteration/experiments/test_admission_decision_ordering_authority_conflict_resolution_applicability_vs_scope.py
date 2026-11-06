import unittest


def evaluate_applicability(scope, resolution):
    return resolution["allowed_scope"] == scope


class TestAdmissionDecisionOrderingAuthorityConflictResolutionApplicabilityVsScope(
    unittest.TestCase
):

    def test_scope_can_exist_without_applicability(self):
        scope = "scope-a"

        self.assertEqual(scope, "scope-a")

    def test_applicability_can_be_observed_for_a_scope(self):
        scope = "scope-a"

        applicability = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        self.assertTrue(applicability)

    def test_same_scope_can_produce_different_applicability(
        self,
    ):
        scope = "scope-a"

        applicability_a = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        applicability_b = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-b",
            },
        )

        self.assertTrue(applicability_a)
        self.assertFalse(applicability_b)

    def test_scope_identity_remains_stable_when_applicability_changes(
        self,
    ):
        scope = "scope-a"

        first = {
            "scope": scope,
            "applicable": True,
        }

        second = {
            "scope": scope,
            "applicable": False,
        }

        self.assertEqual(
            first["scope"],
            second["scope"],
        )

        self.assertNotEqual(
            first["applicable"],
            second["applicable"],
        )

    def test_changing_resolution_can_change_applicability_without_changing_scope(
        self,
    ):
        scope = "scope-a"

        resolution_a = {
            "allowed_scope": "scope-a",
        }

        resolution_b = {
            "allowed_scope": "scope-b",
        }

        applicability_a = evaluate_applicability(
            scope,
            resolution_a,
        )

        applicability_b = evaluate_applicability(
            scope,
            resolution_b,
        )

        self.assertTrue(applicability_a)
        self.assertFalse(applicability_b)

    def test_changing_scope_can_change_applicability_without_mutating_resolution(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        scope_a = "scope-a"
        scope_b = "scope-b"

        applicability_a = evaluate_applicability(
            scope_a,
            resolution,
        )

        applicability_b = evaluate_applicability(
            scope_b,
            resolution,
        )

        self.assertTrue(applicability_a)
        self.assertFalse(applicability_b)

        self.assertEqual(
            resolution["allowed_scope"],
            "scope-a",
        )

    def test_scope_is_not_applicability(self):
        scope = "scope-a"
        applicability = True

        self.assertNotEqual(
            scope,
            applicability,
        )

    def test_scope_identity_is_not_applicability_identity(
        self,
    ):
        scope = {
            "scope_id": "scope-a",
        }

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            id(scope),
            id(applicability),
        )

    def test_applicability_does_not_require_scope_mutation(
        self,
    ):
        scope = {
            "scope_id": "scope-a",
        }

        before = dict(scope)

        applicability = {
            "applicable": True,
            "scope": scope,
        }

        self.assertTrue(
            applicability["applicable"]
        )

        self.assertEqual(
            scope,
            before,
        )

    def test_same_scope_can_be_evaluated_against_multiple_resolutions(
        self,
    ):
        scope = "scope-a"

        resolutions = [
            {
                "allowed_scope": "scope-a",
            },
            {
                "allowed_scope": "scope-b",
            },
            {
                "allowed_scope": "scope-a",
            },
        ]

        results = [
            evaluate_applicability(
                scope,
                resolution,
            )
            for resolution in resolutions
        ]

        self.assertEqual(
            results,
            [True, False, True],
        )

    def test_scope_does_not_determine_applicability_alone(
        self,
    ):
        scope = "scope-a"

        applicability_a = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        applicability_b = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-b",
            },
        )

        self.assertNotEqual(
            applicability_a,
            applicability_b,
        )

    def test_minimal_relationship_preserves_scope_and_applicability_distinction(
        self,
    ):
        scope = "scope-a"
        resolution = {
            "allowed_scope": "scope-a",
        }

        applicable = (
            resolution["allowed_scope"] == scope
        )

        relationship = {
            "scope": scope,
            "resolution": resolution,
            "applicable": applicable,
        }

        self.assertEqual(
            relationship["scope"],
            "scope-a",
        )

        self.assertTrue(
            relationship["applicable"]
        )


if __name__ == "__main__":
    unittest.main()