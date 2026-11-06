import unittest


def evaluate_applicability(scope, resolution):
    return resolution["allowed_scope"] == scope


class TestAdmissionDecisionOrderingAuthorityConflictResolutionApplicabilityVsResolution(
    unittest.TestCase
):

    def test_resolution_can_exist_without_applicability(self):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        self.assertEqual(
            resolution["selected_authority"],
            "authority-a",
        )

    def test_applicability_is_not_resolution_value(self):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        applicability = evaluate_applicability(
            "scope-a",
            resolution,
        )

        self.assertNotEqual(
            resolution,
            applicability,
        )

    def test_same_resolution_can_have_different_applicability(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        applicability_a = evaluate_applicability(
            "scope-a",
            resolution,
        )

        applicability_b = evaluate_applicability(
            "scope-b",
            resolution,
        )

        self.assertTrue(applicability_a)
        self.assertFalse(applicability_b)

    def test_resolution_identity_remains_stable_when_applicability_changes(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        first = {
            "resolution": resolution,
            "applicable": evaluate_applicability(
                "scope-a",
                resolution,
            ),
        }

        second = {
            "resolution": resolution,
            "applicable": evaluate_applicability(
                "scope-b",
                resolution,
            ),
        }

        self.assertIs(
            first["resolution"],
            second["resolution"],
        )

        self.assertNotEqual(
            first["applicable"],
            second["applicable"],
        )

    def test_changing_scope_does_not_mutate_resolution(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        before = dict(resolution)

        evaluate_applicability(
            "scope-b",
            resolution,
        )

        self.assertEqual(
            resolution,
            before,
        )

    def test_same_resolution_can_be_evaluated_in_multiple_contexts(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        contexts = [
            "scope-a",
            "scope-b",
            "scope-a",
        ]

        results = [
            evaluate_applicability(
                scope,
                resolution,
            )
            for scope in contexts
        ]

        self.assertEqual(
            results,
            [True, False, True],
        )

    def test_resolution_semantics_and_applicability_semantics_are_distinct(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        applicability = evaluate_applicability(
            "scope-a",
            resolution,
        )

        self.assertEqual(
            resolution["selected_authority"],
            "authority-a",
        )

        self.assertTrue(applicability)

    def test_resolution_can_be_shared_across_applicability_evaluations(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        evaluation_a = {
            "scope": "scope-a",
            "applicable": evaluate_applicability(
                "scope-a",
                resolution,
            ),
        }

        evaluation_b = {
            "scope": "scope-b",
            "applicable": evaluate_applicability(
                "scope-b",
                resolution,
            ),
        }

        self.assertIsNot(
            evaluation_a,
            evaluation_b,
        )

        self.assertTrue(
            evaluation_a["applicable"]
        )

        self.assertFalse(
            evaluation_b["applicable"]
        )

    def test_changing_resolution_can_change_applicability(
        self,
    ):
        scope = "scope-a"

        resolution_a = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        resolution_b = {
            "selected_authority": "authority-b",
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

    def test_resolution_identity_and_applicability_identity_are_distinct(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        applicability = {
            "applicable": True,
        }

        self.assertNotEqual(
            id(resolution),
            id(applicability),
        )

    def test_applicability_does_not_require_resolution_mutation(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
            "allowed_scope": "scope-a",
        }

        original = dict(resolution)

        result = {
            "resolution": resolution,
            "applicable": evaluate_applicability(
                "scope-a",
                resolution,
            ),
        }

        self.assertTrue(result["applicable"])
        self.assertEqual(
            resolution,
            original,
        )

    def test_minimal_model_preserves_resolution_applicability_distinction(
        self,
    ):
        resolution = "resolution-a"
        scope = "scope-a"

        applicable = (
            resolution == "resolution-a"
            and scope == "scope-a"
        )

        relationship = {
            "resolution": resolution,
            "scope": scope,
            "applicable": applicable,
        }

        self.assertEqual(
            relationship["resolution"],
            "resolution-a",
        )

        self.assertTrue(
            relationship["applicable"]
        )


if __name__ == "__main__":
    unittest.main()