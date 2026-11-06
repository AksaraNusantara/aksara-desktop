import unittest


class EvaluationResult:
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"


class ExecutionDecision:
    PROCEED = "PROCEED"
    DO_NOT_PROCEED = "DO_NOT_PROCEED"


class ExecutionOccurrence:
    def __init__(self, execution_id):
        self.execution_id = execution_id


class EvaluationObservation:
    def __init__(self, result):
        self.result = result


class TestEvaluationVsExecutionDecision(unittest.TestCase):

    def test_evaluation_result_is_distinct_from_execution_decision(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision = ExecutionDecision.PROCEED

        self.assertNotEqual(
            evaluation.result,
            decision,
        )

    def test_allowed_is_not_identical_to_proceed(self):
        self.assertNotEqual(
            EvaluationResult.ALLOWED,
            ExecutionDecision.PROCEED,
        )

    def test_blocked_is_not_identical_to_do_not_proceed(self):
        self.assertNotEqual(
            EvaluationResult.BLOCKED,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_evaluation_result_can_be_used_as_decision_input(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision = (
            ExecutionDecision.PROCEED
            if evaluation.result == EvaluationResult.ALLOWED
            else ExecutionDecision.DO_NOT_PROCEED
        )

        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )

    def test_evaluation_result_does_not_require_execution_decision(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision = None

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertIsNone(decision)

    def test_execution_decision_does_not_require_execution_occurrence(self):
        decision = ExecutionDecision.PROCEED

        execution = None

        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)

    def test_evaluation_result_does_not_create_execution(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        execution = None

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertIsNone(execution)

    def test_blocked_evaluation_can_produce_do_not_proceed_decision(self):
        evaluation = EvaluationObservation(
            EvaluationResult.BLOCKED
        )

        decision = (
            ExecutionDecision.PROCEED
            if evaluation.result == EvaluationResult.ALLOWED
            else ExecutionDecision.DO_NOT_PROCEED
        )

        self.assertEqual(
            decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_same_evaluation_result_can_support_different_decisions_under_different_policies(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        policy_a = "proceed_when_allowed"
        policy_b = "require_additional_confirmation"

        decision_a = (
            ExecutionDecision.PROCEED
            if policy_a == "proceed_when_allowed"
            else ExecutionDecision.DO_NOT_PROCEED
        )

        decision_b = (
            ExecutionDecision.PROCEED
            if policy_b == "proceed_when_allowed"
            else ExecutionDecision.DO_NOT_PROCEED
        )

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )

        self.assertNotEqual(
            decision_a,
            decision_b,
        )

    def test_decision_can_depend_on_inputs_beyond_evaluation_result(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        confirmation_required = True

        decision = (
            ExecutionDecision.DO_NOT_PROCEED
            if confirmation_required
            else ExecutionDecision.PROCEED
        )

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertEqual(
            decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_evaluation_result_can_remain_stable_while_decision_changes(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision_a = ExecutionDecision.PROCEED
        decision_b = ExecutionDecision.DO_NOT_PROCEED

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertNotEqual(
            decision_a,
            decision_b,
        )

    def test_decision_change_does_not_mutate_evaluation_result(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision_a = ExecutionDecision.PROCEED
        decision_b = ExecutionDecision.DO_NOT_PROCEED

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertEqual(
            decision_a,
            ExecutionDecision.PROCEED,
        )
        self.assertEqual(
            decision_b,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_evaluation_result_is_not_execution_state(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        execution_state = None

        self.assertIsNone(execution_state)
        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )

    def test_execution_decision_is_not_execution_occurrence(self):
        decision = ExecutionDecision.PROCEED

        execution_id = None

        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution_id)

    def test_execution_occurrence_can_follow_decision_without_being_identical_to_it(self):
        decision = ExecutionDecision.PROCEED

        execution = ExecutionOccurrence("execution-001")

        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )
        self.assertNotEqual(
            decision,
            execution,
        )

    def test_evaluation_decision_and_execution_form_distinct_boundaries(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision = ExecutionDecision.PROCEED
        execution = None

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)

    def test_semantic_chain_can_be_represented_without_collapsing_results(self):
        evaluation = EvaluationObservation(
            EvaluationResult.ALLOWED
        )

        decision = ExecutionDecision.PROCEED

        execution = None

        self.assertEqual(
            evaluation.result,
            EvaluationResult.ALLOWED,
        )
        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()