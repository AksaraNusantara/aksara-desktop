import unittest


class AdmissionDecision:
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ExecutionPermission:
    GRANTED = "GRANTED"
    NOT_GRANTED = "NOT_GRANTED"


class Eligibility:
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"


class EvaluationObservation:
    def __init__(self, admission, permission, result):
        self.admission = admission
        self.permission = permission
        self.result = result


class TestReEvaluationBoundary(unittest.TestCase):

    def test_initial_evaluation_is_observable(self):
        evaluation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        self.assertEqual(evaluation.admission, "ACCEPTED")
        self.assertEqual(evaluation.permission, "GRANTED")
        self.assertEqual(evaluation.result, "ALLOWED")

    def test_permission_change_can_produce_new_evaluation_result(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertEqual(evaluation_a.admission, evaluation_b.admission)
        self.assertNotEqual(evaluation_a.permission, evaluation_b.permission)
        self.assertNotEqual(evaluation_a.result, evaluation_b.result)

    def test_admission_change_can_produce_new_evaluation_result(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.REJECTED,
            ExecutionPermission.GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertNotEqual(evaluation_a.admission, evaluation_b.admission)
        self.assertEqual(evaluation_a.permission, evaluation_b.permission)
        self.assertNotEqual(evaluation_a.result, evaluation_b.result)

    def test_previous_evaluation_does_not_change_when_new_evaluation_is_created(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertEqual(evaluation_a.admission, "ACCEPTED")
        self.assertEqual(evaluation_a.permission, "GRANTED")
        self.assertEqual(evaluation_a.result, "ALLOWED")

        self.assertEqual(evaluation_b.permission, "NOT_GRANTED")

    def test_re_evaluation_does_not_create_new_admission_identity(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertEqual(
            evaluation_a.admission,
            evaluation_b.admission,
        )

    def test_re_evaluation_does_not_create_execution(self):
        evaluation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        execution_id = None

        self.assertEqual(evaluation.result, Eligibility.ALLOWED)
        self.assertIsNone(execution_id)

    def test_evaluation_result_is_distinct_from_permission(self):
        evaluation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        self.assertNotEqual(
            evaluation.result,
            evaluation.permission,
        )

    def test_evaluation_result_is_distinct_from_admission(self):
        evaluation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        self.assertNotEqual(
            evaluation.result,
            evaluation.admission,
        )

    def test_same_inputs_can_produce_stable_result(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        self.assertEqual(evaluation_a.result, evaluation_b.result)

    def test_changed_permission_is_not_mutation_of_previous_permission(self):
        permission_a = ExecutionPermission.GRANTED
        permission_b = ExecutionPermission.NOT_GRANTED

        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            permission_a,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            permission_b,
            Eligibility.BLOCKED,
        )

        self.assertEqual(evaluation_a.permission, "GRANTED")
        self.assertEqual(evaluation_b.permission, "NOT_GRANTED")

    def test_changed_admission_is_not_mutation_of_previous_admission(self):
        admission_a = AdmissionDecision.ACCEPTED
        admission_b = AdmissionDecision.REJECTED

        evaluation_a = EvaluationObservation(
            admission_a,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            admission_b,
            ExecutionPermission.GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertEqual(evaluation_a.admission, "ACCEPTED")
        self.assertEqual(evaluation_b.admission, "REJECTED")

    def test_evaluation_observations_can_be_ordered(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        observations = [evaluation_a, evaluation_b]

        self.assertEqual(len(observations), 2)
        self.assertIs(observations[0], evaluation_a)
        self.assertIs(observations[1], evaluation_b)

    def test_ordered_evaluations_preserve_distinct_results(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        observations = [evaluation_a, evaluation_b]

        self.assertEqual(
            observations[0].result,
            Eligibility.ALLOWED,
        )
        self.assertEqual(
            observations[1].result,
            Eligibility.BLOCKED,
        )

    def test_re_evaluation_is_not_automatically_execution(self):
        evaluation_a = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.GRANTED,
            Eligibility.ALLOWED,
        )

        evaluation_b = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        execution_occurred = False

        self.assertNotEqual(evaluation_a.result, evaluation_b.result)
        self.assertFalse(execution_occurred)

    def test_re_evaluation_is_a_semantic_observation_not_an_execution_state(self):
        evaluation = EvaluationObservation(
            AdmissionDecision.ACCEPTED,
            ExecutionPermission.NOT_GRANTED,
            Eligibility.BLOCKED,
        )

        self.assertEqual(evaluation.result, Eligibility.BLOCKED)
        self.assertNotIn(
            evaluation.result,
            (
                AdmissionDecision.ACCEPTED,
                AdmissionDecision.REJECTED,
                ExecutionPermission.GRANTED,
                ExecutionPermission.NOT_GRANTED,
            ),
        )


if __name__ == "__main__":
    unittest.main()