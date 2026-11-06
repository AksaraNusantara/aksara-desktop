import unittest
from dataclasses import dataclass
from enum import Enum


class Authority(Enum):
    SYSTEM = "system"
    USER = "user"


class Permission(Enum):
    GRANTED = "granted"
    NOT_GRANTED = "not_granted"


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


@dataclass(frozen=True)
class PermissionObservation:
    request_id: str
    authority: Authority
    permission: Permission


@dataclass(frozen=True)
class ExecutionDecisionObservation:
    request_id: str
    authority: Authority
    decision: ExecutionDecision


class TestAuthorityIdentityAcrossContexts(unittest.TestCase):

    def test_same_authority_can_participate_in_permission_evaluation(self):
        observation = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        self.assertEqual(
            observation.authority,
            Authority.SYSTEM,
        )

    def test_same_authority_can_participate_in_execution_decision(self):
        observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            observation.authority,
            Authority.SYSTEM,
        )

    def test_authority_identity_can_remain_same_across_contexts(self):
        permission_observation = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision_observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            permission_observation.authority,
            decision_observation.authority,
        )

    def test_same_authority_can_support_different_semantic_results(self):
        permission_observation = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision_observation = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            permission_observation.authority,
            decision_observation.authority,
        )

        self.assertNotEqual(
            permission_observation.permission,
            decision_observation.decision,
        )

    def test_authority_is_not_permission(self):
        self.assertNotEqual(
            Authority.SYSTEM,
            Permission.GRANTED,
        )

    def test_authority_is_not_execution_decision(self):
        self.assertNotEqual(
            Authority.SYSTEM,
            ExecutionDecision.PROCEED,
        )

    def test_permission_context_does_not_change_authority_identity(self):
        first = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        second = PermissionObservation(
            request_id="REQ-002",
            authority=Authority.SYSTEM,
            permission=Permission.NOT_GRANTED,
        )

        self.assertEqual(
            first.authority,
            second.authority,
        )

    def test_execution_context_does_not_change_authority_identity(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-002",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            first.authority,
            second.authority,
        )

    def test_same_authority_can_appear_in_multiple_requests(self):
        observations = [
            PermissionObservation(
                request_id="REQ-001",
                authority=Authority.SYSTEM,
                permission=Permission.GRANTED,
            ),
            ExecutionDecisionObservation(
                request_id="REQ-002",
                authority=Authority.SYSTEM,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(
            {
                observation.authority
                for observation in observations
            },
            {Authority.SYSTEM},
        )

    def test_different_authorities_can_participate_in_same_semantic_context(self):
        observations = [
            PermissionObservation(
                request_id="REQ-001",
                authority=Authority.SYSTEM,
                permission=Permission.GRANTED,
            ),
            PermissionObservation(
                request_id="REQ-001",
                authority=Authority.USER,
                permission=Permission.NOT_GRANTED,
            ),
        ]

        self.assertEqual(
            {
                observation.authority
                for observation in observations
            },
            {
                Authority.SYSTEM,
                Authority.USER,
            },
        )

    def test_different_authorities_can_participate_in_execution_context(self):
        observations = [
            ExecutionDecisionObservation(
                request_id="REQ-001",
                authority=Authority.SYSTEM,
                decision=ExecutionDecision.PROCEED,
            ),
            ExecutionDecisionObservation(
                request_id="REQ-001",
                authority=Authority.USER,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
        ]

        self.assertEqual(
            {
                observation.authority
                for observation in observations
            },
            {
                Authority.SYSTEM,
                Authority.USER,
            },
        )

    def test_authority_change_does_not_intrinsically_define_permission(self):
        first = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        second = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.USER,
            permission=Permission.GRANTED,
        )

        self.assertNotEqual(
            first.authority,
            second.authority,
        )

        self.assertEqual(
            first.permission,
            second.permission,
        )

    def test_authority_change_does_not_intrinsically_define_execution_decision(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.USER,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(
            first.authority,
            second.authority,
        )

        self.assertEqual(
            first.decision,
            second.decision,
        )

    def test_permission_change_does_not_change_authority_identity(self):
        first = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        second = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.NOT_GRANTED,
        )

        self.assertEqual(
            first.authority,
            second.authority,
        )

        self.assertNotEqual(
            first.permission,
            second.permission,
        )

    def test_execution_decision_change_does_not_change_authority_identity(self):
        first = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        second = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            first.authority,
            second.authority,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_authority_identity_can_cross_semantic_boundaries(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            permission.authority,
            decision.authority,
        )

    def test_permission_and_execution_decision_remain_distinct_results(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertNotEqual(
            permission.permission,
            decision.decision,
        )

    def test_authority_is_shared_without_collapsing_result_semantics(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            permission.authority,
            decision.authority,
        )

        self.assertEqual(
            permission.permission,
            Permission.GRANTED,
        )

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

    def test_semantic_model_can_reuse_authority_without_creating_execution_authority_type(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertIs(
            type(permission.authority),
            type(decision.authority),
        )

    def test_authority_identity_is_not_defined_by_its_result(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(
            permission.authority,
            decision.authority,
        )

        self.assertNotEqual(
            permission.permission,
            decision.decision,
        )

    def test_cross_context_authority_reuse_does_not_require_new_request(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(
            permission.request_id,
            decision.request_id,
        )

        self.assertEqual(
            permission.authority,
            decision.authority,
        )

    def test_cross_context_authority_identity_remains_independent_from_execution(self):
        permission = PermissionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            permission=Permission.GRANTED,
        )

        decision = ExecutionDecisionObservation(
            request_id="REQ-001",
            authority=Authority.SYSTEM,
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(
            permission.authority,
            decision.authority,
        )

        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()