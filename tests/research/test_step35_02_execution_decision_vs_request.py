import unittest
from dataclasses import dataclass
from enum import Enum


class ExecutionDecision(Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str


@dataclass(frozen=True)
class DecisionObservation:
    request_id: str
    decision: ExecutionDecision


class TestExecutionDecisionVsRequest(unittest.TestCase):

    def test_request_identity_is_distinct_from_decision_value(self):
        request = ExecutionRequest("REQ-001")
        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotEqual(request, decision)
        self.assertEqual(request.request_id, decision.request_id)

    def test_request_can_exist_without_decision(self):
        request = ExecutionRequest("REQ-001")

        self.assertIsNotNone(request)
        self.assertEqual(request.request_id, "REQ-001")

    def test_decision_can_exist_without_execution(self):
        decision = DecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertIsNotNone(decision)
        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )

    def test_same_request_can_have_multiple_decision_observations(self):
        request = ExecutionRequest("REQ-001")

        observations = [
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(len(observations), 2)
        self.assertTrue(
            all(obs.request_id == request.request_id for obs in observations)
        )

    def test_decision_change_does_not_require_new_request_identity(self):
        request = ExecutionRequest("REQ-001")

        first = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        second = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(first.request_id, second.request_id)
        self.assertEqual(first.request_id, request.request_id)

    def test_different_decisions_can_reference_same_request(self):
        request = ExecutionRequest("REQ-001")

        decisions = {
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
        }

        self.assertEqual(
            {d.request_id for d in decisions},
            {request.request_id},
        )

    def test_decision_does_not_mutate_request_identity(self):
        request = ExecutionRequest("REQ-001")

        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        self.assertEqual(request.request_id, "REQ-001")
        self.assertEqual(decision.request_id, "REQ-001")

    def test_request_identity_is_stable_across_decisions(self):
        request = ExecutionRequest("REQ-001")

        observations = [
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
        ]

        self.assertEqual(
            [obs.request_id for obs in observations],
            ["REQ-001", "REQ-001", "REQ-001"],
        )

    def test_request_is_not_decision(self):
        request = ExecutionRequest("REQ-001")

        self.assertNotIsInstance(
            request,
            ExecutionDecision,
        )

    def test_decision_is_not_request(self):
        decision = DecisionObservation(
            request_id="REQ-001",
            decision=ExecutionDecision.PROCEED,
        )

        self.assertNotIsInstance(
            decision,
            ExecutionRequest,
        )

    def test_do_not_proceed_does_not_destroy_request(self):
        request = ExecutionRequest("REQ-001")

        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.DO_NOT_PROCEED,
        )

        self.assertEqual(request.request_id, decision.request_id)

    def test_proceed_does_not_create_execution(self):
        request = ExecutionRequest("REQ-001")

        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)

    def test_multiple_decisions_do_not_imply_multiple_requests(self):
        request = ExecutionRequest("REQ-001")

        decisions = [
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        request_ids = {decision.request_id for decision in decisions}

        self.assertEqual(request_ids, {"REQ-001"})

    def test_request_to_decision_relationship_can_be_one_to_many(self):
        request = ExecutionRequest("REQ-001")

        decisions = [
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.DO_NOT_PROCEED,
            ),
            DecisionObservation(
                request_id=request.request_id,
                decision=ExecutionDecision.PROCEED,
            ),
        ]

        self.assertEqual(len(decisions), 2)
        self.assertEqual(
            len({d.request_id for d in decisions}),
            1,
        )

    def test_decision_observation_is_distinct_from_request_lifecycle(self):
        request = ExecutionRequest("REQ-001")

        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        lifecycle_observation = "QUEUED"

        self.assertEqual(decision.request_id, request.request_id)
        self.assertEqual(lifecycle_observation, "QUEUED")

    def test_semantic_boundary_request_decision_execution(self):
        request = ExecutionRequest("REQ-001")

        decision = DecisionObservation(
            request_id=request.request_id,
            decision=ExecutionDecision.PROCEED,
        )

        execution = None

        self.assertEqual(request.request_id, decision.request_id)
        self.assertEqual(
            decision.decision,
            ExecutionDecision.PROCEED,
        )
        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()