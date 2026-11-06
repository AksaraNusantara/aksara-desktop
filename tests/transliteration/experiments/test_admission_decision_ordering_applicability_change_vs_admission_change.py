import unittest


def evaluate_admission(
    applicable,
    capacity_available,
    policy,
):
    if policy == "require_applicability":
        if not applicable:
            return "REJECTED"

    if not capacity_available:
        return "REJECTED"

    return "ACCEPTED"


class TestAdmissionDecisionOrderingApplicabilityChangeVsAdmissionChange(
    unittest.TestCase
):

    def test_applicability_change_can_change_admission(self):
        accepted = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="require_applicability",
        )

        rejected = evaluate_admission(
            applicable=False,
            capacity_available=True,
            policy="require_applicability",
        )

        self.assertEqual(
            accepted,
            "ACCEPTED",
        )

        self.assertEqual(
            rejected,
            "REJECTED",
        )

    def test_applicability_change_does_not_always_change_admission(
        self,
    ):
        first = evaluate_admission(
            applicable=True,
            capacity_available=False,
            policy="require_applicability",
        )

        second = evaluate_admission(
            applicable=False,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertEqual(
            first,
            "REJECTED",
        )

        self.assertEqual(
            second,
            "REJECTED",
        )

    def test_same_admission_result_can_span_different_applicability(
        self,
    ):
        result_a = evaluate_admission(
            applicable=True,
            capacity_available=False,
            policy="require_applicability",
        )

        result_b = evaluate_admission(
            applicable=False,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertEqual(
            result_a,
            result_b,
        )

    def test_applicability_change_can_be_observed_without_mutating_admission_observation(
        self,
    ):
        admission = {
            "decision": "ACCEPTED",
        }

        first_applicability = True
        second_applicability = False

        self.assertEqual(
            admission["decision"],
            "ACCEPTED",
        )

        self.assertNotEqual(
            first_applicability,
            second_applicability,
        )

        self.assertEqual(
            admission["decision"],
            "ACCEPTED",
        )

    def test_admission_can_be_reconsidered_after_applicability_change(
        self,
    ):
        first = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="require_applicability",
        )

        second = evaluate_admission(
            applicable=False,
            capacity_available=True,
            policy="require_applicability",
        )

        self.assertEqual(
            first,
            "ACCEPTED",
        )

        self.assertEqual(
            second,
            "REJECTED",
        )

    def test_reconsideration_does_not_require_mutating_previous_decision(
        self,
    ):
        previous_decision = "ACCEPTED"

        new_decision = "REJECTED"

        history = [
            previous_decision,
            new_decision,
        ]

        self.assertEqual(
            history[0],
            "ACCEPTED",
        )

        self.assertEqual(
            history[1],
            "REJECTED",
        )

    def test_applicability_can_change_while_scope_identity_is_unchanged(
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

    def test_applicability_can_change_while_resolution_identity_is_unchanged(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
        }

        first = {
            "resolution": resolution,
            "applicable": True,
        }

        second = {
            "resolution": resolution,
            "applicable": False,
        }

        self.assertIs(
            first["resolution"],
            second["resolution"],
        )

        self.assertNotEqual(
            first["applicable"],
            second["applicable"],
        )

    def test_admission_result_depends_on_more_than_applicability(
        self,
    ):
        result_a = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="require_applicability",
        )

        result_b = evaluate_admission(
            applicable=True,
            capacity_available=False,
            policy="require_applicability",
        )

        self.assertNotEqual(
            result_a,
            result_b,
        )

    def test_policy_can_change_effect_of_applicability_change(
        self,
    ):
        strict_before = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="require_applicability",
        )

        strict_after = evaluate_admission(
            applicable=False,
            capacity_available=True,
            policy="require_applicability",
        )

        permissive_before = evaluate_admission(
            applicable=True,
            capacity_available=True,
            policy="ignore_applicability",
        )

        permissive_after = evaluate_admission(
            applicable=False,
            capacity_available=True,
            policy="ignore_applicability",
        )

        self.assertEqual(
            strict_before,
            "ACCEPTED",
        )

        self.assertEqual(
            strict_after,
            "REJECTED",
        )

        self.assertEqual(
            permissive_before,
            "ACCEPTED",
        )

        self.assertEqual(
            permissive_after,
            "ACCEPTED",
        )

    def test_applicability_change_does_not_require_new_scope_identity(
        self,
    ):
        scope = "scope-a"

        observations = [
            {
                "scope": scope,
                "applicable": True,
            },
            {
                "scope": scope,
                "applicable": False,
            },
        ]

        self.assertEqual(
            observations[0]["scope"],
            observations[1]["scope"],
        )

    def test_applicability_change_does_not_require_new_resolution_identity(
        self,
    ):
        resolution = {
            "selected_authority": "authority-a",
        }

        observations = [
            {
                "resolution": resolution,
                "applicable": True,
            },
            {
                "resolution": resolution,
                "applicable": False,
            },
        ]

        self.assertIs(
            observations[0]["resolution"],
            observations[1]["resolution"],
        )

    def test_minimal_model_preserves_independent_change(
        self,
    ):
        observations = [
            {
                "applicable": True,
                "admission": "ACCEPTED",
            },
            {
                "applicable": False,
                "admission": "ACCEPTED",
            },
        ]

        self.assertNotEqual(
            observations[0]["applicable"],
            observations[1]["applicable"],
        )

        self.assertEqual(
            observations[0]["admission"],
            observations[1]["admission"],
        )


if __name__ == "__main__":
    unittest.main()