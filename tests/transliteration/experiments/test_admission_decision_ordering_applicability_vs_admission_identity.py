import unittest


class ExperimentalApplicability:
    def __init__(self, applicable):
        self.applicable = applicable


class ExperimentalAdmissionDecision:
    def __init__(self, decision):
        self.decision = decision


class TestAdmissionDecisionOrderingApplicabilityVsAdmissionIdentity(
    unittest.TestCase
):

    def test_applicability_and_admission_have_distinct_types(self):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        self.assertNotEqual(
            type(applicability),
            type(admission),
        )

    def test_applicability_can_exist_without_admission(self):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        self.assertTrue(
            applicability.applicable
        )

    def test_admission_can_exist_without_applicability(self):
        admission = ExperimentalAdmissionDecision(
            decision="REJECTED",
        )

        self.assertEqual(
            admission.decision,
            "REJECTED",
        )

    def test_applicability_is_not_admission_value(self):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        self.assertNotEqual(
            applicability.applicable,
            admission.decision,
        )

    def test_applicability_identity_is_not_admission_identity(self):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        self.assertNotEqual(
            id(applicability),
            id(admission),
        )

    def test_changing_applicability_does_not_require_mutating_admission(
        self,
    ):
        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        first_applicability = ExperimentalApplicability(
            applicable=True,
        )

        second_applicability = ExperimentalApplicability(
            applicable=False,
        )

        self.assertTrue(
            first_applicability.applicable
        )

        self.assertFalse(
            second_applicability.applicable
        )

        self.assertEqual(
            admission.decision,
            "ACCEPTED",
        )

    def test_changing_admission_does_not_require_mutating_applicability(
        self,
    ):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        first_admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        second_admission = ExperimentalAdmissionDecision(
            decision="REJECTED",
        )

        self.assertTrue(
            applicability.applicable
        )

        self.assertEqual(
            first_admission.decision,
            "ACCEPTED",
        )

        self.assertEqual(
            second_admission.decision,
            "REJECTED",
        )

        self.assertTrue(
            applicability.applicable
        )

    def test_same_applicability_can_be_observed_with_multiple_admission_decisions(
        self,
    ):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        admission_a = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        admission_b = ExperimentalAdmissionDecision(
            decision="REJECTED",
        )

        self.assertTrue(
            applicability.applicable
        )

        self.assertNotEqual(
            admission_a.decision,
            admission_b.decision,
        )

    def test_same_admission_decision_can_be_observed_with_different_applicability(
        self,
    ):
        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        applicability_a = ExperimentalApplicability(
            applicable=True,
        )

        applicability_b = ExperimentalApplicability(
            applicable=False,
        )

        self.assertEqual(
            admission.decision,
            "ACCEPTED",
        )

        self.assertNotEqual(
            applicability_a.applicable,
            applicability_b.applicable,
        )

    def test_neither_requires_the_other_as_identity(self):
        applicability = ExperimentalApplicability(
            applicable=True,
        )

        admission = ExperimentalAdmissionDecision(
            decision="ACCEPTED",
        )

        self.assertTrue(
            applicability.applicable
        )

        self.assertEqual(
            admission.decision,
            "ACCEPTED",
        )

    def test_applicability_does_not_require_admission_id(self):
        applicability = {
            "applicable": True,
        }

        self.assertNotIn(
            "admission_id",
            applicability,
        )

    def test_admission_does_not_require_applicability_id(self):
        admission = {
            "decision": "ACCEPTED",
        }

        self.assertNotIn(
            "applicability_id",
            admission,
        )

    def test_minimal_model_preserves_identity_distinction(self):
        applicability = {
            "applicable": True,
        }

        admission = {
            "decision": "ACCEPTED",
        }

        self.assertTrue(
            applicability["applicable"]
        )

        self.assertEqual(
            admission["decision"],
            "ACCEPTED",
        )

        self.assertNotEqual(
            applicability,
            admission,
        )


if __name__ == "__main__":
    unittest.main()