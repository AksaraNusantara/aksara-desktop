import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


class ExecutionAuthority(Enum):
    AUTHORIZED = "authorized"
    NOT_AUTHORIZED = "not_authorized"


class ExecutionTrigger(Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"


@dataclass(frozen=True)
class ExecutionDecisionObservation:
    request_id: str
    decision: ExecutionDecision


@dataclass(frozen=True)
class ExecutionAuthorityObservation:
    request_id: str
    authority: ExecutionAuthority


@dataclass(frozen=True)
class ExecutionTriggerObservation:
    request_id: str
    trigger: ExecutionTrigger


class TestExecutionDecisionVsExecutionAuthority(unittest.TestCase):

    def test_execution_decision_is_distinct_from_execution_authority(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        self.assertNotEqual(decision, authority)

    def test_proceed_is_not_identical_to_authorized(self):
        self.assertNotEqual(
            ExecutionDecision.PROCEED,
            ExecutionAuthority.AUTHORIZED,
        )

    def test_do_not_proceed_is_not_identical_to_not_authorized(self):
        self.assertNotEqual(
            ExecutionDecision.DO_NOT_PROCEED,
            ExecutionAuthority.NOT_AUTHORIZED,
        )

    def test_execution_decision_can_exist_without_execution_authority(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = None

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertIsNone(authority)

    def test_execution_authority_can_exist_without_execution_decision(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        decision = None

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

        self.assertIsNone(decision)

    def test_proceed_can_coexist_with_not_authorized(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.NOT_AUTHORIZED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.NOT_AUTHORIZED,
        )

    def test_do_not_proceed_can_coexist_with_authorized(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

    def test_same_decision_can_have_different_authority(self):
        authorized = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        not_authorized = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.NOT_AUTHORIZED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            authorized.authority,
            not_authorized.authority,
        )

    def test_same_authority_can_support_different_decisions(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        proceed = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        do_not_proceed = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

        self.assertNotEqual(
            proceed.decision,
            do_not_proceed.decision,
        )

    def test_authority_change_does_not_require_decision_change(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        first = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        second = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.NOT_AUTHORIZED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            first.authority,
            second.authority,
        )

    def test_decision_change_does_not_require_authority_change(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_authority_is_not_execution_decision(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        self.assertFalse(
            isinstance(
                authority,
                ExecutionDecisionObservation,
            )
        )

    def test_execution_decision_is_not_authority(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertFalse(
            isinstance(
                decision,
                ExecutionAuthorityObservation,
            )
        )

    def test_authority_does_not_create_execution_decision(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        decision = None

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

        self.assertIsNone(decision)

    def test_execution_decision_does_not_create_authority(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = None

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

        self.assertIsNone(authority)

    def test_execution_authority_does_not_create_trigger(self):
        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        trigger = None

        self.assertEqual(
            authority.authority,
            ExecutionAuthority.AUTHORIZED,
        )

        self.assertIsNone(trigger)

    def test_execution_decision_does_not_create_trigger(self):
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

    def test_decision_and_authority_can_be_combined_as_inputs(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        inputs = (
            decision.decision,
            authority.authority,
        )

        self.assertEqual(len(inputs), 2)

    def test_same_request_can_have_multiple_authority_observations(self):
        observations = [
            ExecutionAuthorityObservation(
                request_id="REQ-001",
                authority=ExecutionAuthority.NOT_AUTHORIZED,
            ),
            ExecutionAuthorityObservation(
                request_id="REQ-001",
                authority=ExecutionAuthority.AUTHORIZED,
            ),
        ]

        self.assertEqual(len(observations), 2)

        self.assertEqual(
            {observation.request_id for observation in observations},
            {"REQ-001"},
        )

    def test_same_request_can_have_multiple_decision_observations(self):
        observations = [
            ExecutionDecisionObservation(
                request_id="REQ-001",
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            ExecutionDecisionObservation(
                request_id="REQ-001",
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(len(observations), 2)

        self.assertEqual(
            {observation.request_id for observation in observations},
            {"REQ-001"},
        )

    def test_decision_and_authority_have_distinct_semantic_roles(self):
        decision = ExecutionDecision.PROCEED
        authority = ExecutionAuthority.AUTHORIZED

        self.assertNotEqual(decision, authority)

    def test_decision_authority_and_trigger_remain_distinct(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertNotEqual(decision.decision, authority.authority)
        self.assertNotEqual(authority.authority, trigger.trigger)
        self.assertNotEqual(decision.decision, trigger.trigger)

    def test_semantic_chain_can_be_represented_without_collapsing_boundaries(self):
        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        authority = ExecutionAuthorityObservation(
            request_id="REQ-001",
            authority=ExecutionAuthority.AUTHORIZED,
        )

        trigger = ExecutionTriggerObservation(
            request_id="REQ-001",
            trigger=ExecutionTrigger.TRIGGERED,
        )

        self.assertEqual(
            decision.request_id,
            authority.request_id,
        )

        self.assertEqual(
            authority.request_id,
            trigger.request_id,
        )


if __name__ == "__main__":
    unittest.main()