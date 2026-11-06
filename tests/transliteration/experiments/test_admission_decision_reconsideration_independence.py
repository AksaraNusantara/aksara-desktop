import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalAdmissionDecision(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalAdmissionDecisionObservation:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionDecisionReconsiderationIndependence(unittest.TestCase):

    def test_same_request_with_two_decisions_is_representable(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            2,
        )

    def test_reconsideration_can_be_inferred_without_special_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        same_request = (
            observations[0].request.request_id
            == observations[1].request.request_id
        )

        changed_decision = (
            observations[0].decision
            != observations[1].decision
        )

        self.assertTrue(same_request)
        self.assertTrue(changed_decision)

    def test_reconsideration_does_not_require_request_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            request.request_id,
            original_request_id,
        )

        for observation in observations:
            self.assertEqual(
                observation.request.request_id,
                original_request_id,
            )

    def test_reconsideration_does_not_require_decision_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            second.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

    def test_reconsideration_does_not_require_history_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        observations = [first, second]

        self.assertEqual(
            observations[0].request.request_id,
            observations[1].request.request_id,
        )

    def test_reconsideration_does_not_require_orchestration_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        orchestration = None

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertIsNone(orchestration)

    def test_reconsideration_does_not_require_admission_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        admission_object = None

        self.assertEqual(
            len(observations),
            2,
        )

        self.assertIsNone(admission_object)

    def test_reconsideration_does_not_require_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        execution = None

        self.assertEqual(
            observations[0].request.request_id,
            observations[1].request.request_id,
        )

        self.assertIsNone(execution)

    def test_same_decision_can_still_be_reconsidered(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(
            observations[0].request.request_id,
            observations[1].request.request_id,
        )

        self.assertEqual(
            observations[0].decision,
            observations[1].decision,
        )

    def test_multiple_reconsiderations_need_no_special_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        self.assertEqual(
            len(observations),
            3,
        )

        for observation in observations:
            self.assertEqual(
                observation.request.request_id,
                request.request_id,
            )

    def test_reconsideration_semantics_are_separate_from_execution_semantics(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        execution_state = None

        self.assertEqual(
            observations[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            observations[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution_state)

    def test_minimal_request_decision_model_preserves_reconsideration_information(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        observations = [
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmissionDecisionObservation(
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        same_request = all(
            observation.request.request_id
            == request.request_id
            for observation in observations
        )

        decision_changed = (
            observations[0].decision
            != observations[1].decision
        )

        self.assertTrue(same_request)
        self.assertTrue(decision_changed)


if __name__ == "__main__":
    unittest.main()