import unittest
from dataclasses import dataclass
from enum import Enum


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class EvaluationResult(Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"


class Permission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


@dataclass(frozen=True)
class ExecutionDecisionObservation:
    request_id: str
    admission: AdmissionDecision
    evaluation: EvaluationResult
    permission: Permission
    decision: ExecutionDecision


class TestAdmissionAsExecutionDecisionInput(unittest.TestCase):

    def test_admission_can_be_an_input_to_execution_decision(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            observation.decision,
            ExecutionDecision.PROCEED,
        )

    def test_admission_is_not_execution_decision(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            observation.admission,
            observation.decision,
        )

    def test_accepted_alone_does_not_determine_proceed(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.BLOCKED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            first.admission,
            second.admission,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_rejected_can_be_observed_with_do_not_proceed(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.REJECTED,
            evaluation=EvaluationResult.BLOCKED,
            permission=Permission.NOT_GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            observation.decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_rejected_does_not_need_to_be_identical_to_do_not_proceed(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.REJECTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            observation.admission,
            AdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observation.decision,
            ExecutionDecision.PROCEED,
        )

    def test_same_admission_different_evaluation_can_change_decision(self):
        blocked = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.BLOCKED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        allowed = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(blocked.admission, allowed.admission)
        self.assertNotEqual(blocked.decision, allowed.decision)

    def test_same_admission_different_permission_can_change_decision(self):
        not_granted = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.NOT_GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        granted = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            not_granted.admission,
            granted.admission,
        )

        self.assertNotEqual(
            not_granted.decision,
            granted.decision,
        )

    def test_same_admission_same_evaluation_same_permission_can_support_different_decisions_under_context(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(first.admission, second.admission)
        self.assertEqual(first.evaluation, second.evaluation)
        self.assertEqual(first.permission, second.permission)
        self.assertNotEqual(first.decision, second.decision)

    def test_admission_does_not_create_execution_decision(self):
        admission = AdmissionDecision.ACCEPTED

        execution_decision = None

        self.assertEqual(
            admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution_decision)

    def test_execution_decision_can_exist_without_execution(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(
            observation.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertIsNone(execution)

    def test_admission_can_remain_stable_while_evaluation_changes(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.BLOCKED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(first.admission, second.admission)
        self.assertNotEqual(first.evaluation, second.evaluation)

    def test_admission_can_remain_stable_while_permission_changes(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.NOT_GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(first.admission, second.admission)
        self.assertNotEqual(first.permission, second.permission)

    def test_admission_is_one_input_among_multiple_inputs(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        inputs = (
            observation.admission,
            observation.evaluation,
            observation.permission,
        )

        self.assertEqual(len(inputs), 3)

    def test_execution_decision_is_distinct_from_all_inputs(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(observation.decision, observation.admission)
        self.assertNotEqual(observation.decision, observation.evaluation)
        self.assertNotEqual(observation.decision, observation.permission)

    def test_same_admission_can_support_multiple_decision_observations(self):
        observations = [
            ExecutionDecisionObservation(
                request_id="REQ-001",
                admission=AdmissionDecision.ACCEPTED,
                evaluation=EvaluationResult.BLOCKED,
                permission=Permission.GRANTED,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            ExecutionDecisionObservation(
                request_id="REQ-001",
                admission=AdmissionDecision.ACCEPTED,
                evaluation=EvaluationResult.ALLOWED,
                permission=Permission.GRANTED,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(len(observations), 2)

        self.assertTrue(
            all(
                observation.admission == AdmissionDecision.ACCEPTED
                for observation in observations
            )
        )

    def test_decision_change_does_not_mutate_admission(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.BLOCKED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            first.admission,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            second.admission,
            AdmissionDecision.ACCEPTED,
        )

    def test_admission_as_input_does_not_collapse_semantic_boundaries(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            admission=AdmissionDecision.ACCEPTED,
            evaluation=EvaluationResult.ALLOWED,
            permission=Permission.GRANTED,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertIsInstance(
            observation.admission,
            AdmissionDecision,
        )

        self.assertIsInstance(
            observation.evaluation,
            EvaluationResult,
        )

        self.assertIsInstance(
            observation.permission,
            Permission,
        )

        self.assertIsInstance(
            observation.decision,
            ExecutionDecision,
        )


if __name__ == "__main__":
    unittest.main()