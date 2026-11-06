import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionState(Enum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETED = "completed"


class AdmissionDecision(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class EvaluationResult(Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


class ExecutionTrigger(Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"


@dataclass(frozen=True)
class SemanticObservation:
    request_id: str
    value: Enum


class TestStateVsDecisionVsObservation(unittest.TestCase):

    def test_execution_state_is_distinct_from_admission_decision(self):
        state = ExecutionState.NOT_STARTED
        admission = AdmissionDecision.ACCEPTED

        self.assertNotEqual(state, admission)

    def test_execution_state_is_distinct_from_evaluation_result(self):
        state = ExecutionState.NOT_STARTED
        evaluation = EvaluationResult.ALLOWED

        self.assertNotEqual(state, evaluation)

    def test_execution_state_is_distinct_from_execution_decision(self):
        state = ExecutionState.NOT_STARTED
        decision = ExecutionDecision.PROCEED

        self.assertNotEqual(state, decision)

    def test_execution_state_is_distinct_from_execution_trigger(self):
        state = ExecutionState.NOT_STARTED
        trigger = ExecutionTrigger.TRIGGERED

        self.assertNotEqual(state, trigger)

    def test_admission_decision_is_distinct_from_evaluation_result(self):
        admission = AdmissionDecision.ACCEPTED
        evaluation = EvaluationResult.ALLOWED

        self.assertNotEqual(admission, evaluation)

    def test_admission_decision_is_distinct_from_execution_decision(self):
        admission = AdmissionDecision.ACCEPTED
        decision = ExecutionDecision.PROCEED

        self.assertNotEqual(admission, decision)

    def test_admission_decision_is_distinct_from_execution_trigger(self):
        admission = AdmissionDecision.ACCEPTED
        trigger = ExecutionTrigger.TRIGGERED

        self.assertNotEqual(admission, trigger)

    def test_evaluation_result_is_distinct_from_execution_decision(self):
        evaluation = EvaluationResult.ALLOWED
        decision = ExecutionDecision.PROCEED

        self.assertNotEqual(evaluation, decision)

    def test_evaluation_result_is_distinct_from_execution_trigger(self):
        evaluation = EvaluationResult.ALLOWED
        trigger = ExecutionTrigger.TRIGGERED

        self.assertNotEqual(evaluation, trigger)

    def test_execution_decision_is_distinct_from_execution_trigger(self):
        decision = ExecutionDecision.PROCEED
        trigger = ExecutionTrigger.TRIGGERED

        self.assertNotEqual(decision, trigger)

    def test_same_request_can_have_multiple_semantic_dimensions(self):
        observations = [
            SemanticObservation(
                request_id="REQ-001",
                value=AdmissionDecision.ACCEPTED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=EvaluationResult.ALLOWED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionDecision.PROCEED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionTrigger.TRIGGERED,
            ),
        ]

        self.assertEqual(len(observations), 4)

        self.assertEqual(
            {observation.request_id for observation in observations},
            {"REQ-001"},
        )

    def test_semantic_observation_does_not_require_execution_state_change(self):
        state = ExecutionState.NOT_STARTED

        observation = SemanticObservation(
            request_id="REQ-001",
            value=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            observation.value,
            ExecutionDecision.PROCEED,
        )

    def test_execution_decision_can_exist_while_state_is_not_started(self):
        state = ExecutionState.NOT_STARTED

        decision = SemanticObservation(
            request_id="REQ-001",
            value=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            decision.value,
            ExecutionDecision.PROCEED,
        )

    def test_trigger_can_exist_while_state_is_not_started(self):
        state = ExecutionState.NOT_STARTED

        trigger = SemanticObservation(
            request_id="REQ-001",
            value=ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            trigger.value,
            ExecutionTrigger.TRIGGERED,
        )

    def test_evaluation_can_exist_while_state_is_not_started(self):
        state = ExecutionState.NOT_STARTED

        evaluation = SemanticObservation(
            request_id="REQ-001",
            value=EvaluationResult.ALLOWED,
        )

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            evaluation.value,
            EvaluationResult.ALLOWED,
        )

    def test_admission_can_exist_while_state_is_not_started(self):
        state = ExecutionState.NOT_STARTED

        admission = SemanticObservation(
            request_id="REQ-001",
            value=AdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            admission.value,
            AdmissionDecision.ACCEPTED,
        )

    def test_state_change_does_not_require_decision_change(self):
        first_state = ExecutionState.NOT_STARTED
        second_state = ExecutionState.RUNNING

        decision = ExecutionDecision.PROCEED

        self.assertNotEqual(first_state, second_state)

        self.assertEqual(
            decision,
            ExecutionDecision.PROCEED,
        )

    def test_decision_change_does_not_require_state_change(self):
        state = ExecutionState.NOT_STARTED

        first_decision = ExecutionDecision.DO_NOT_PROCEED
        second_decision = ExecutionDecision.PROCEED

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertNotEqual(first_decision, second_decision)

    def test_trigger_change_does_not_require_state_change(self):
        state = ExecutionState.NOT_STARTED

        first_trigger = ExecutionTrigger.NOT_TRIGGERED
        second_trigger = ExecutionTrigger.TRIGGERED

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertNotEqual(first_trigger, second_trigger)

    def test_evaluation_change_does_not_require_state_change(self):
        state = ExecutionState.NOT_STARTED

        first_evaluation = EvaluationResult.BLOCKED
        second_evaluation = EvaluationResult.ALLOWED

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertNotEqual(first_evaluation, second_evaluation)

    def test_admission_change_does_not_require_state_change(self):
        state = ExecutionState.NOT_STARTED

        first_admission = AdmissionDecision.ACCEPTED
        second_admission = AdmissionDecision.REJECTED

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertNotEqual(first_admission, second_admission)

    def test_semantic_observations_do_not_become_execution_state(self):
        observation = SemanticObservation(
            request_id="REQ-001",
            value=ExecutionDecision.PROCEED,
        )

        self.assertIsInstance(
            observation.value,
            ExecutionDecision,
        )

        self.assertNotIsInstance(
            observation.value,
            ExecutionState,
        )

    def test_multiple_observation_types_can_coexist(self):
        observations = [
            SemanticObservation(
                request_id="REQ-001",
                value=AdmissionDecision.ACCEPTED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=EvaluationResult.ALLOWED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionDecision.PROCEED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionTrigger.TRIGGERED,
            ),
        ]

        self.assertEqual(
            len(observations),
            4,
        )

        self.assertEqual(
            len(
                {
                    type(observation.value)
                    for observation in observations
                }
            ),
            4,
        )

    def test_execution_state_can_coexist_with_observations(self):
        state = ExecutionState.NOT_STARTED

        observations = [
            SemanticObservation(
                request_id="REQ-001",
                value=AdmissionDecision.ACCEPTED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=EvaluationResult.ALLOWED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionDecision.PROCEED,
            ),
            SemanticObservation(
                request_id="REQ-001",
                value=ExecutionTrigger.TRIGGERED,
            ),
        ]

        self.assertEqual(
            state,
            ExecutionState.NOT_STARTED,
        )

        self.assertEqual(
            len(observations),
            4,
        )

    def test_semantic_taxonomy_can_be_represented_without_collapsing_categories(self):
        state = ExecutionState.NOT_STARTED
        admission = AdmissionDecision.ACCEPTED
        evaluation = EvaluationResult.ALLOWED
        decision = ExecutionDecision.PROCEED
        trigger = ExecutionTrigger.TRIGGERED

        values = [
            state,
            admission,
            evaluation,
            decision,
            trigger,
        ]

        self.assertEqual(len(values), 5)

        self.assertEqual(
            len({type(value) for value in values}),
            5,
        )


if __name__ == "__main__":
    unittest.main()