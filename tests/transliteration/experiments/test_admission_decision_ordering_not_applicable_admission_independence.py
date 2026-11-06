import unittest


def evaluate_applicability(scope, resolution):
    return resolution["allowed_scope"] == scope


def evaluate_admission(applicable, admission_policy):
    if admission_policy == "reject_if_not_applicable":
        return "REJECTED"

    return admission_policy


class TestAdmissionDecisionOrderingNotApplicableAdmissionIndependence(
    unittest.TestCase
):

    def test_not_applicable_can_be_rejected(self):
        applicable = False

        admission = evaluate_admission(
            applicable,
            "reject_if_not_applicable",
        )

        self.assertFalse(applicable)
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_not_applicable_does_not_define_admission_value_by_itself(
        self,
    ):
        applicable = False

        admission = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertFalse(applicable)
        self.assertEqual(
            admission,
            "DEFERRED",
        )

    def test_not_applicable_can_exist_before_admission(
        self,
    ):
        applicable = False

        self.assertFalse(applicable)

    def test_same_not_applicable_result_can_be_associated_with_different_admission_outcomes(
        self,
    ):
        applicable = False

        admission_a = evaluate_admission(
            applicable,
            "REJECTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertEqual(
            admission_a,
            "REJECTED",
        )

        self.assertEqual(
            admission_b,
            "DEFERRED",
        )

    def test_admission_policy_can_define_how_not_applicable_is_handled(
        self,
    ):
        applicable = False

        rejected = evaluate_admission(
            applicable,
            "reject_if_not_applicable",
        )

        deferred = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertEqual(
            rejected,
            "REJECTED",
        )

        self.assertEqual(
            deferred,
            "DEFERRED",
        )

    def test_changing_admission_policy_does_not_change_applicability(
        self,
    ):
        applicable = False

        admission_a = evaluate_admission(
            applicable,
            "REJECTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertFalse(applicable)
        self.assertNotEqual(
            admission_a,
            admission_b,
        )

    def test_resolution_can_remain_unchanged_while_admission_policy_changes(
        self,
    ):
        resolution = {
            "allowed_scope": "scope-a",
        }

        scope = "scope-b"

        applicable = evaluate_applicability(
            scope,
            resolution,
        )

        admission_a = evaluate_admission(
            applicable,
            "REJECTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertFalse(applicable)
        self.assertNotEqual(
            admission_a,
            admission_b,
        )

        self.assertEqual(
            resolution["allowed_scope"],
            "scope-a",
        )

    def test_scope_can_remain_unchanged_while_admission_policy_changes(
        self,
    ):
        scope = "scope-b"

        applicable = evaluate_applicability(
            scope,
            {
                "allowed_scope": "scope-a",
            },
        )

        admission_a = evaluate_admission(
            applicable,
            "REJECTED",
        )

        admission_b = evaluate_admission(
            applicable,
            "DEFERRED",
        )

        self.assertFalse(applicable)
        self.assertNotEqual(
            admission_a,
            admission_b,
        )

    def test_not_applicable_is_not_equal_to_rejected(
        self,
    ):
        applicable = False
        admission = "REJECTED"

        self.assertNotEqual(
            applicable,
            admission,
        )

    def test_not_applicable_is_not_an_admission_identity(
        self,
    ):
        applicability = {
            "applicable": False,
        }

        admission = {
            "decision": "REJECTED",
        }

        self.assertNotEqual(
            id(applicability),
            id(admission),
        )

    def test_applicability_can_be_observed_without_mutating_admission(
        self,
    ):
        admission = {
            "decision": "DEFERRED",
        }

        applicable = False

        observation = {
            "applicable": applicable,
            "admission": admission,
        }

        self.assertFalse(
            observation["applicable"]
        )

        self.assertEqual(
            admission["decision"],
            "DEFERRED",
        )

    def test_admission_can_use_not_applicable_as_one_input(
        self,
    ):
        applicable = False

        other_input = {
            "capacity_available": True,
        }

        admission = (
            "REJECTED"
            if not applicable
            else "ACCEPTED"
        )

        self.assertFalse(applicable)
        self.assertTrue(
            other_input["capacity_available"]
        )
        self.assertEqual(
            admission,
            "REJECTED",
        )

    def test_minimal_model_preserves_independence(self):
        applicable = False

        admission = "DEFERRED"

        relationship = {
            "applicable": applicable,
            "admission": admission,
        }

        self.assertFalse(
            relationship["applicable"]
        )

        self.assertEqual(
            relationship["admission"],
            "DEFERRED",
        )


if __name__ == "__main__":
    unittest.main()