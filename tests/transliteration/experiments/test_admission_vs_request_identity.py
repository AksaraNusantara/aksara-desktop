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


class TestAdmissionVsRequestIdentity(unittest.TestCase):

    def test_request_identity_is_stable_across_admissions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.002",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            "req.001",
        )

        self.assertEqual(
            second.request.request_id,
            "req.001",
        )

    def test_admission_identity_does_not_define_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.003",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.admission_id,
            request.request_id,
        )

    def test_changing_admission_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        ExperimentalAdmission(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        ExperimentalAdmission(
            admission_id="adm.005",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            request.request_id,
            original_request_id,
        )

    def test_distinct_admissions_can_reference_identical_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
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
            first.request,
            second.request,
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )

    def test_admission_identity_is_not_derived_from_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.008",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.009",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.decision,
            second.decision,
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )

    def test_admission_identity_is_not_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.010",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.admission_id,
            request.request_id,
        )

    def test_multiple_admissions_preserve_single_request_reference(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        admissions = [
            ExperimentalAdmission(
                admission_id="adm.011",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.012",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.013",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        request_ids = {
            admission.request.request_id
            for admission in admissions
        }

        self.assertEqual(
            request_ids,
            {"req.007"},
        )

    def test_request_identity_survives_reconsideration(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        rejected = ExperimentalAdmission(
            admission_id="adm.014",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        accepted = ExperimentalAdmission(
            admission_id="adm.015",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            rejected.request.request_id,
            accepted.request.request_id,
        )

    def test_admission_identity_can_change_while_request_identity_remains_stable(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first_admission = ExperimentalAdmission(
            admission_id="adm.016",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second_admission = ExperimentalAdmission(
            admission_id="adm.017",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first_admission.admission_id,
            second_admission.admission_id,
        )

        self.assertEqual(
            first_admission.request.request_id,
            second_admission.request.request_id,
        )

    def test_admission_identity_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.018",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.019",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.operation.operation_id,
            second.request.operation.operation_id,
        )

    def test_request_identity_is_parent_reference_not_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.020",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            admission.request.request_id,
            request.request_id,
        )

        self.assertNotEqual(
            admission.admission_id,
            request.request_id,
        )

    def test_admission_identity_remains_distinct_even_when_request_content_is_identical(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.021",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.022",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request,
            second.request,
        )

        self.assertEqual(
            first.decision,
            second.decision,
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )


if __name__ == "__main__":
    unittest.main()