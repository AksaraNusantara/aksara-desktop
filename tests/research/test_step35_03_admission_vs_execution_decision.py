import unittest
from dataclasses import dataclass
from enum import Enum


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str


@dataclass(frozen=True)
class AdmissionObservation:
    request_id: str
    decision: AdmissionDecision


@dataclass(frozen=True)
class ExecutionDecisionObservation:
    request_id: str
    decision: ExecutionDecision


class TestAdmissionVsExecutionDecision(unittest.TestCase):

    def test_admission_decision_is_distinct_from_execution_decision(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(admission, execution_decision)

    def test_accepted_is_not_identical_to_proceed(self):
        self.assertNotEqual(
            AdmissionDecision.ACCEPTED,
            ExecutionDecision.PROCEED,
        )

    def test_rejected_is_not_identical_to_do_not_proceed(self):
        self.assertNotEqual(
            AdmissionDecision.REJECTED,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_admission_can_exist_without_execution_decision(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = None

        self.assertEqual(
            admission.decision,
            AdmissionDecision.ACCEPTED,
        )
        self.assertIsNone(execution_decision)

    def test_execution_decision_can_exist_without_execution(self):
        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(
            execution_decision.decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)

    def test_accepted_does_not_imply_proceed(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            admission.decision,
            AdmissionDecision.ACCEPTED,
        )
        self.assertEqual(
            execution_decision.decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_rejected_does_not_require_do_not_proceed_as_same_decision(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.REJECTED,
        )

        execution_decision = None

        self.assertEqual(
            admission.decision,
            AdmissionDecision.REJECTED,
        )
        self.assertIsNone(execution_decision)

    def test_admission_and_execution_decision_are_separate_observations(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            admission.request_id,
            execution_decision.request_id,
        )

        self.assertNotEqual(
            type(admission),
            type(execution_decision),
        )

    def test_same_request_can_have_admission_and_execution_decision(self):
        request = ExecutionRequest("REQ-001")

        admission = AdmissionObservation(
            request_id=request.request_id,
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(admission.request_id, request.request_id)
        self.assertEqual(
            execution_decision.request_id,
            request.request_id,
        )

    def test_admission_can_remain_stable_while_execution_decision_changes(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            admission.decision,
            AdmissionDecision.ACCEPTED,
        )
        self.assertNotEqual(first.decision, second.decision)

    def test_execution_decision_can_remain_stable_while_admission_changes(self):
        first_admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second_admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.REJECTED,
        )

        self.assertNotEqual(
            first_admission.decision,
            second_admission.decision,
        )
        self.assertEqual(
            execution_decision.decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_one_admission_can_be_related_to_multiple_execution_decisions(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        decisions = [
            ExecutionDecisionObservation(
                request_id=admission.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            ExecutionDecisionObservation(
                request_id=admission.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(len(decisions), 2)
        self.assertTrue(
            all(
                decision.request_id == admission.request_id
                for decision in decisions
            )
        )

    def test_multiple_admissions_can_exist_for_same_request(self):
        request = ExecutionRequest("REQ-001")

        admissions = [
            AdmissionObservation(
                request_id=request.request_id,
                decision=AdmissionDecision.ACCEPTED,
            ),
            AdmissionObservation(
                request_id=request.request_id,
                decision=AdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(len(admissions), 2)
        self.assertEqual(
            {admission.request_id for admission in admissions},
            {request.request_id},
        )

    def test_admission_identity_is_not_execution_decision_identity(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            id(admission),
            id(execution_decision),
        )

    def test_execution_decision_does_not_mutate_admission(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            admission.decision,
            AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            execution_decision.decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

    def test_admission_does_not_create_execution_decision(self):
        admission = AdmissionObservation(
            request_id="REQ-001",
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = None

        self.assertIsNotNone(admission)
        self.assertIsNone(execution_decision)

    def test_execution_decision_does_not_create_execution(self):
        execution_decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(
            execution_decision.decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)

    def test_admission_and_execution_decision_can_have_different_semantic_inputs(self):
        admission_input = "admission_policy"
        execution_decision_input = "execution_policy"

        self.assertNotEqual(
            admission_input,
            execution_decision_input,
        )

    def test_decision_boundaries_can_be_represented_without_collapsing_them(self):
        request = ExecutionRequest("REQ-001")

        admission = AdmissionObservation(
            request_id=request.request_id,
            decision=AdmissionDecision.ACCEPTED,
        )

        execution_decision = ExecutionDecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(request.request_id, admission.request_id)
        self.assertEqual(
            request.request_id,
            execution_decision.request_id,
        )

        self.assertIsInstance(
            admission.decision,
            AdmissionDecision,
        )

        self.assertIsInstance(
            execution_decision.decision,
            ExecutionDecision,
        )


if __name__ == "__main__":
    unittest.main()