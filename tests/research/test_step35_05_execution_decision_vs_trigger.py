import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


class ExecutionTrigger(Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"


@dataclass(frozen=True)
class ExecutionDecisionObservation:
    request_id: str
    decision: ExecutionDecision


@dataclass(frozen=True)
class ExecutionTriggerObservation:
    request_id: str
    trigger: ExecutionTrigger


@dataclass(frozen=True)
class ExecutionOccurrence:
    execution_id: str
    request_id: str


class TestExecutionDecisionVsTrigger(unittest.TestCase):

    def test_execution_decision_is_distinct_from_trigger(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertNotEqual(decision, trigger)

    def test_proceed_is_not_identical_to_triggered(self):
        self.assertNotEqual(
            ExecutionDecision.PROCEED,
            ExecutionTrigger.TRIGGERED,
        )

    def test_do_not_proceed_is_not_identical_to_not_triggered(self):
        self.assertNotEqual(
            ExecutionDecision.DO_NOT_PROCEED,
            ExecutionTrigger.NOT_TRIGGERED,
        )

    def test_proceed_can_exist_without_trigger(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = None

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertIsNone(trigger)

    def test_trigger_can_exist_without_execution(self):
        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = None

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.TRIGGERED,
        )

        self.assertIsNone(execution)

    def test_same_decision_can_have_different_trigger_observations(self):
        first = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        second = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.NOT_TRIGGERED,
        )

        self.assertNotEqual(
            first.trigger,
            second.trigger,
        )

    def test_decision_can_remain_stable_while_trigger_changes(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        first_trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.NOT_TRIGGERED,
        )

        second_trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            first_trigger.trigger,
            second_trigger.trigger,
        )

    def test_trigger_does_not_create_execution_occurrence(self):
        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = None

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.TRIGGERED,
        )

        self.assertIsNone(execution)

    def test_execution_occurrence_is_distinct_from_trigger(self):
        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = ExecutionOccurrence(
            execution_id="EXEC-001",
            request_id="REQ-001",
        )

        self.assertNotEqual(trigger, execution)

    def test_execution_occurrence_is_distinct_from_decision(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        execution = ExecutionOccurrence(
            execution_id="EXEC-001",
            request_id="REQ-001",
        )

        self.assertNotEqual(decision, execution)

    def test_proceed_can_be_followed_by_not_triggered(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.NOT_TRIGGERED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.NOT_TRIGGERED,
        )

    def test_proceed_can_be_followed_by_triggered(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.TRIGGERED,
        )

    def test_triggered_can_be_followed_by_execution(self):
        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = ExecutionOccurrence(
            execution_id="EXEC-001",
            request_id="REQ-001",
        )

        self.assertEqual(
            trigger.request_id,
            execution.request_id,
        )

    def test_decision_does_not_mutate_trigger(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.NOT_TRIGGERED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.NOT_TRIGGERED,
        )

    def test_trigger_does_not_mutate_decision(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.TRIGGERED,
        )

    def test_multiple_trigger_observations_can_reference_same_request(self):
        observations = [
            ExecutionTriggerObservation(
                request_id="REQ-001",
                trigger=ExecutionTrigger.NOT_TRIGGERED,
            ),
            ExecutionTriggerObservation(
                request_id="REQ-001",
                trigger=ExecutionTrigger.TRIGGERED,
            ),
        ]

        self.assertEqual(len(observations), 2)

        self.assertEqual(
            {observation.request_id for observation in observations},
            {"REQ-001"},
        )

    def test_multiple_executions_can_follow_triggering(self):
        executions = [
            ExecutionOccurrence(
                execution_id="EXEC-001",
                request_id="REQ-001",
            ),
            ExecutionOccurrence(
                execution_id="EXEC-002",
                request_id="REQ-001",
            ),
        ]

        self.assertEqual(len(executions), 2)

        self.assertEqual(
            {execution.request_id for execution in executions},
            {"REQ-001"},
        )

    def test_request_identity_is_shared_but_semantic_boundaries_remain_distinct(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = ExecutionOccurrence(
            execution_id="EXEC-001",
            request_id="REQ-001",
        )

        self.assertEqual(decision.request_id, trigger.request_id)
        self.assertEqual(trigger.request_id, execution.request_id)

        self.assertNotEqual(decision.decision, trigger.trigger)
        self.assertNotEqual(trigger.trigger, execution.execution_id)

    def test_semantic_chain_can_be_represented_without_collapsing_boundaries(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        execution = ExecutionOccurrence(
            execution_id="EXEC-001",
            request_id="REQ-001",
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            trigger.trigger,
            ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            execution.request_id,
            "REQ-001",
        )


if __name__ == "__main__":
    unittest.main()