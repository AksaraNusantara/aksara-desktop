import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalRequestState(Enum):
    CREATED = auto()
    ACCEPTED = auto()
    REJECTED = auto()


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
class ExperimentalAdmission:
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestRequestStateVsAdmission(unittest.TestCase):

    def test_request_exists_before_admission_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertEqual(
            request.request_id,
            "req.001",
        )

    def test_admission_decision_does_not_create_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.002",
        )

    def test_accepted_is_not_execution_state(self):
        execution_states = {
            "SUCCESS",
            "FAILED",
            "NOT_EXECUTED",
        }

        self.assertNotIn(
            "ACCEPTED",
            execution_states,
        )

    def test_rejected_is_not_execution_state(self):
        execution_states = {
            "SUCCESS",
            "FAILED",
            "NOT_EXECUTED",
        }

        self.assertNotIn(
            "REJECTED",
            execution_states,
        )

    def test_admission_decision_is_independent_of_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            admission.request.request_id,
            "req.003",
        )

        self.assertIsNone(execution_id)

    def test_rejected_request_can_have_no_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution_id = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution_id)

    def test_accepted_request_can_still_have_no_execution_yet(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIsNone(execution_id)

    def test_admission_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.operation.operation_id,
            "op.transliterate",
        )

    def test_same_request_identity_can_be_observed_with_different_admission_attempts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_request_state_model_and_admission_model_have_different_semantics(self):
        request_state = ExperimentalRequestState.ACCEPTED
        admission_decision = ExperimentalAdmissionDecision.ACCEPTED

        self.assertEqual(
            request_state.name,
            admission_decision.name,
        )

        self.assertNotEqual(
            type(request_state),
            type(admission_decision),
        )

    def test_admission_decision_is_an_external_relationship_to_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertIs(
            admission.request,
            request,
        )

    def test_request_identity_survives_without_any_admission_object(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertEqual(
            request.request_id,
            "req.010",
        )


if __name__ == "__main__":
    unittest.main()