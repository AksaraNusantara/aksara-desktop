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


@dataclass(frozen=True)
class ExperimentalReconsiderationObservation:
    request: ExperimentalExecutionRequest


class TestAdmissionDecisionReconsideration(unittest.TestCase):

    def test_reconsideration_can_reference_same_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            reconsideration.request.request_id,
            request.request_id,
        )

    def test_reconsideration_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            reconsideration.request.request_id,
            "req.002",
        )

    def test_reconsideration_can_produce_new_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=reconsideration.request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_reconsideration_does_not_require_mutating_previous_decision(self):
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

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=reconsideration.request,
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

    def test_reconsideration_is_distinct_from_decision_value(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        decision = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            decision.request.request_id,
            reconsideration.request.request_id,
        )

        self.assertIsNot(
            decision,
            reconsideration,
        )

    def test_reconsideration_can_be_represented_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        execution = None

        self.assertEqual(
            reconsideration.request.request_id,
            request.request_id,
        )

        self.assertIsNone(execution)

    def test_reconsideration_can_happen_multiple_times(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration_1 = ExperimentalReconsiderationObservation(
            request=request
        )

        reconsideration_2 = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            reconsideration_1.request.request_id,
            reconsideration_2.request.request_id,
        )

        self.assertIsNot(
            reconsideration_1,
            reconsideration_2,
        )

    def test_reconsideration_does_not_require_request_mutation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            request.request_id,
            original_request_id,
        )

        self.assertEqual(
            reconsideration.request.request_id,
            original_request_id,
        )

    def test_reconsideration_can_preserve_same_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmissionDecisionObservation(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        second = ExperimentalAdmissionDecisionObservation(
            request=reconsideration.request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            first.decision,
            second.decision,
        )

    def test_reconsideration_is_not_itself_an_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        execution = None

        self.assertIsNotNone(reconsideration)
        self.assertIsNone(execution)

    def test_reconsideration_can_exist_without_explicit_event_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            reconsideration.request,
            request,
        )

    def test_reconsideration_does_not_require_reconsideration_id(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        reconsideration = ExperimentalReconsiderationObservation(
            request=request
        )

        self.assertEqual(
            reconsideration.request.request_id,
            request.request_id,
        )


if __name__ == "__main__":
    unittest.main()