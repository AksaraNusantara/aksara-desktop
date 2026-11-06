import unittest


def evaluate_admission(
    applicable,
    policy,
):
    if policy == "require_applicability":
        return "ACCEPTED" if applicable else "REJECTED"

    if policy == "ignore_applicability":
        return "ACCEPTED"

    return "DEFERRED"


class TestAdmissionDecisionOrderingMinimalApplicabilityAdmissionRelationship(
    unittest.TestCase
):

    def test_applicability_can_be_represented_independently(self):
        applicability = True

        self.assertTrue(applicability)

    def test_admission_can_be_represented_independently(self):
        admission = "ACCEPTED"

        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_relationship_can_connect_applicability_and_admission(
        self,
    ):
        applicability = True

        admission = evaluate_admission(
            applicability,
            "require_applicability",
        )

        self.assertTrue(applicability)
        self.assertEqual(
            admission,
            "ACCEPTED",
        )

    def test_applicability_need_not_be_stored_inside_admission(
        self,
    ):
        admission = {
            "decision": "ACCEPTED",
        }

        self.assertNotIn(
            "applicable",
            admission,
        )

    def test_admission_need_not_be_stored_inside_applicability(
        self,
    ):
        applicability = {
            "applicable": True,
        }

        self.assertNotIn(
            "decision",
            applicability,
        )

    def test_policy_can_define_relationship_without_mutating_applicability(
        self,
    ):
        applicability = True

        first = evaluate_admission(
            applicability,
            "require_applicability",
        )

        second = evaluate_admission(
            applicability,
            "ignore_applicability",
        )

        self.assertEqual(first, "ACCEPTED")
        self.assertEqual(second, "ACCEPTED")
        self.assertTrue(applicability)

    def test_policy_can_define_different_relationship_for_false_applicability(
        self,
    ):
        applicability = False

        strict = evaluate_admission(
            applicability,
            "require_applicability",
        )

        permissive = evaluate_admission(
            applicability,
            "ignore_applicability",
        )

        deferred = evaluate_admission(
            applicability,
            "defer_on_uncertain_applicability",
        )

        self.assertEqual(strict, "REJECTED")
        self.assertEqual(permissive, "ACCEPTED")
        self.assertEqual(deferred, "DEFERRED")

    def test_same_applicability_can_support_multiple_admission_results(
        self,
    ):
        applicability = False

        results = [
            evaluate_admission(
                applicability,
                "require_applicability",
            ),
            evaluate_admission(
                applicability,
                "ignore_applicability",
            ),
            evaluate_admission(
                applicability,
                "defer_on_uncertain_applicability",
            ),
        ]

        self.assertEqual(
            results,
            [
                "REJECTED",
                "ACCEPTED",
                "DEFERRED",
            ],
        )

    def test_admission_result_does_not_change_applicability_identity(
        self,
    ):
        applicability = {
            "applicable": False,
        }

        admission = evaluate_admission(
            applicability["applicable"],
            "require_applicability",
        )

        self.assertEqual(
            admission,
            "REJECTED",
        )

        self.assertFalse(
            applicability["applicable"]
        )

    def test_applicability_result_does_not_change_admission_identity(
        self,
    ):
        admission = {
            "decision": "ACCEPTED",
        }

        applicability = False

        self.assertEqual(
            admission["decision"],
            "ACCEPTED",
        )

        self.assertFalse(applicability)

    def test_minimal_relationship_needs_no_relationship_id(
        self,
    ):
        relationship = {
            "applicable": True,
            "decision": "ACCEPTED",
        }

        self.assertNotIn(
            "relationship_id",
            relationship,
        )

    def test_minimal_relationship_needs_no_applicability_object(
        self,
    ):
        applicable = True
        decision = evaluate_admission(
            applicable,
            "require_applicability",
        )

        self.assertEqual(
            decision,
            "ACCEPTED",
        )

    def test_minimal_relationship_needs_no_admission_object(
        self,
    ):
        applicable = True

        decision = (
            "ACCEPTED"
            if applicable
            else "REJECTED"
        )

        self.assertEqual(
            decision,
            "ACCEPTED",
        )

    def test_minimal_model_preserves_both_semantics(self):
        applicable = False

        decision = evaluate_admission(
            applicable,
            "ignore_applicability",
        )

        relationship = {
            "applicable": applicable,
            "decision": decision,
        }

        self.assertFalse(
            relationship["applicable"]
        )

        self.assertEqual(
            relationship["decision"],
            "ACCEPTED",
        )


if __name__ == "__main__":
    unittest.main()