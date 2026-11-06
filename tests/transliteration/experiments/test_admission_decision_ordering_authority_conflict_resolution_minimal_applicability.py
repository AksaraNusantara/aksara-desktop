import unittest


def evaluate_applicability(requirement, resolution):
    return requirement == resolution


class TestAdmissionDecisionOrderingAuthorityConflictResolutionMinimalApplicability(
    unittest.TestCase
):

    def test_requirement_and_resolution_can_produce_applicability(self):
        requirement = "authority-a"
        resolution = "authority-a"

        applicable = evaluate_applicability(
            requirement,
            resolution,
        )

        self.assertTrue(applicable)

    def test_different_requirement_and_resolution_produce_not_applicable(
        self,
    ):
        requirement = "authority-a"
        resolution = "authority-b"

        applicable = evaluate_applicability(
            requirement,
            resolution,
        )

        self.assertFalse(applicable)

    def test_minimal_model_needs_no_applicability_object(self):
        requirement = "authority-a"
        resolution = "authority-a"

        applicable = (
            requirement == resolution
        )

        self.assertTrue(applicable)

    def test_minimal_model_needs_no_applicability_id(self):
        requirement = "authority-a"
        resolution = "authority-a"

        applicable = (
            requirement == resolution
        )

        observation = {
            "applicable": applicable,
        }

        self.assertNotIn(
            "applicability_id",
            observation,
        )

    def test_resolution_can_exist_without_applicability_result(
        self,
    ):
        resolution = "authority-a"

        self.assertEqual(
            resolution,
            "authority-a",
        )

    def test_requirement_can_exist_without_applicability_result(
        self,
    ):
        requirement = "authority-a"

        self.assertEqual(
            requirement,
            "authority-a",
        )

    def test_applicability_does_not_require_resolution_mutation(
        self,
    ):
        requirement = "authority-a"
        resolution = {
            "selected_authority": "authority-a",
        }

        before = dict(resolution)

        applicable = (
            requirement
            == resolution["selected_authority"]
        )

        self.assertTrue(applicable)
        self.assertEqual(
            resolution,
            before,
        )

    def test_applicability_does_not_require_requirement_mutation(
        self,
    ):
        requirement = {
            "required_authority": "authority-a",
        }

        resolution = "authority-a"

        before = dict(requirement)

        applicable = (
            requirement["required_authority"]
            == resolution
        )

        self.assertTrue(applicable)
        self.assertEqual(
            requirement,
            before,
        )

    def test_same_resolution_can_be_evaluated_against_multiple_requirements(
        self,
    ):
        resolution = "authority-a"

        requirements = [
            "authority-a",
            "authority-b",
            "authority-a",
        ]

        results = [
            evaluate_applicability(
                requirement,
                resolution,
            )
            for requirement in requirements
        ]

        self.assertEqual(
            results,
            [True, False, True],
        )

    def test_same_requirement_can_be_evaluated_against_multiple_resolutions(
        self,
    ):
        requirement = "authority-a"

        resolutions = [
            "authority-a",
            "authority-b",
            "authority-a",
        ]

        results = [
            evaluate_applicability(
                requirement,
                resolution,
            )
            for resolution in resolutions
        ]

        self.assertEqual(
            results,
            [True, False, True],
        )

    def test_policy_can_be_added_without_becoming_applicability_identity(
        self,
    ):
        requirement = "authority-a"
        resolution = "authority-a"

        policy = {
            "enabled": True,
        }

        applicable = (
            policy["enabled"]
            and requirement == resolution
        )

        self.assertTrue(applicable)

        self.assertNotIn(
            "applicability_id",
            policy,
        )

    def test_minimal_relationship_can_preserve_both_participants(
        self,
    ):
        requirement = "authority-a"
        resolution = "authority-a"

        relationship = {
            "requirement": requirement,
            "resolution": resolution,
            "applicable": (
                requirement == resolution
            ),
        }

        self.assertEqual(
            relationship["requirement"],
            "authority-a",
        )

        self.assertEqual(
            relationship["resolution"],
            "authority-a",
        )

        self.assertTrue(
            relationship["applicable"]
        )


if __name__ == "__main__":
    unittest.main()