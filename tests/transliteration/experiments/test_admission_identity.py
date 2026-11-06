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
class ExperimentalAdmission:
    admission_id: str
    request: ExperimentalExecutionRequest
    decision: ExperimentalAdmissionDecision


class TestAdmissionIdentity(unittest.TestCase):

    def test_request_has_identity_independent_of_admission(self):
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

    def test_admission_has_its_own_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.admission_id,
            "adm.001",
        )

    def test_admission_identity_differs_from_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.admission_id,
            admission.request.request_id,
        )

    def test_admission_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.002",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            "req.004",
        )

    def test_admission_preserves_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.003",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.operation.operation_id,
            "op.transliterate",
        )

    def test_admission_can_be_represented_without_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            admission.admission_id,
            "adm.004",
        )

        self.assertIsNone(execution_id)

    def test_rejected_admission_can_have_identity_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.005",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution_id = None

        self.assertEqual(
            admission.admission_id,
            "adm.005",
        )

        self.assertIsNone(execution_id)

    def test_two_admissions_can_reference_same_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.006",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.007",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_two_admissions_can_have_distinct_identities(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.008",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.009",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )

    def test_admission_identity_is_not_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.010",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = "exec.001"

        self.assertNotEqual(
            admission.admission_id,
            execution_id,
        )

    def test_admission_identity_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        ExperimentalAdmission(
            admission_id="adm.011",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            request.request_id,
            original_request_id,
        )

    def test_admission_identity_can_exist_before_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.012",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            admission.admission_id,
            "adm.012",
        )

        self.assertIsNone(execution_id)


if __name__ == "__main__":
    unittest.main()