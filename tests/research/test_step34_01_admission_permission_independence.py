import unittest


class AdmissionDecision:
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class EvaluationObservation:
    def __init__(self, admission, permission):
        self.admission = admission
        self.permission = permission


class TestAdmissionPermissionIndependence(unittest.TestCase):

    def test_accepted_and_granted_are_distinct_dimensions(self):
        observation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )
        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )
        self.assertNotEqual(
            observation.admission,
            observation.permission,
        )

    def test_accepted_and_not_granted_are_representable(self):
        observation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )
        self.assertEqual(
            observation.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_rejected_and_granted_are_representable(self):
        observation = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.REJECTED,
        )
        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

    def test_rejected_and_not_granted_are_representable(self):
        observation = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.REJECTED,
        )
        self.assertEqual(
            observation.permission,
            ExecutionPermission.NOT_GRANTED,
        )

    def test_permission_does_not_identify_admission(self):
        granted_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        granted_b = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            granted_a.permission,
            granted_b.permission,
        )
        self.assertNotEqual(
            granted_a.admission,
            granted_b.admission,
        )

    def test_admission_does_not_identify_permission(self):
        accepted_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        accepted_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            accepted_a.admission,
            accepted_b.admission,
        )
        self.assertNotEqual(
            accepted_a.permission,
            accepted_b.permission,
        )

    def test_permission_change_does_not_require_admission_change(self):
        observation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        observation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation_a.admission,
            observation_b.admission,
        )
        self.assertNotEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_admission_change_does_not_require_permission_change(self):
        observation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        observation_b = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
        )

        self.assertNotEqual(
            observation_a.admission,
            observation_b.admission,
        )
        self.assertEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_granted_does_not_imply_accepted(self):
        observation = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )
        self.assertNotEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )

    def test_accepted_does_not_imply_granted(self):
        observation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )
        self.assertNotEqual(
            observation.permission,
            ExecutionPermission.GRANTED,
        )

    def test_admission_and_permission_can_be_observed_without_execution(self):
        observation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        execution_occurred = False

        self.assertIsNotNone(observation.admission)
        self.assertIsNotNone(observation.permission)
        self.assertFalse(execution_occurred)

    def test_admission_and_permission_are_not_execution(self):
        observation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        execution_id = None

        self.assertIsNone(execution_id)
        self.assertIsNotNone(observation.admission)
        self.assertIsNotNone(observation.permission)

    def test_same_admission_permission_pair_can_be_observed_multiple_times(self):
        observation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        observation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
        )

        self.assertEqual(
            observation_a.admission,
            observation_b.admission,
        )
        self.assertEqual(
            observation_a.permission,
            observation_b.permission,
        )

    def test_permission_is_not_an_admission_state(self):
        self.assertNotIn(
            ExecutionPermission.GRANTED,
            (
                AdmissionDecision.ACCEPTED,
                AdmissionDecision.REJECTED,
            ),
        )
        self.assertNotIn(
            ExecutionPermission.NOT_GRANTED,
            (
                AdmissionDecision.ACCEPTED,
                AdmissionDecision.REJECTED,
            ),
        )

    def test_admission_is_not_a_permission_state(self):
        self.assertNotIn(
            AdmissionDecision.ACCEPTED,
            (
                ExecutionPermission.GRANTED,
                ExecutionPermission.NOT_GRANTED,
            ),
        )
        self.assertNotIn(
            AdmissionDecision.REJECTED,
            (
                ExecutionPermission.GRANTED,
                ExecutionPermission.NOT_GRANTED,
            ),
        )


if __name__ == "__main__":
    unittest.main()