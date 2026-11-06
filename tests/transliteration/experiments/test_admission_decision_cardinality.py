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


class TestAdmissionDecisionCardinality(unittest.TestCase):

    def test_request_can_have_one_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.001",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admissions = [admission]

        self.assertEqual(
            len(admissions),
            1,
        )

    def test_request_can_be_associated_with_multiple_admissions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.002",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.003",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admissions = [first, second]

        self.assertEqual(
            len(admissions),
            2,
        )

    def test_multiple_admissions_preserve_same_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.005",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

    def test_multiple_admissions_can_have_distinct_decisions(self):
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

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_multiple_admissions_have_distinct_identities(self):
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

    def test_admission_cardinality_does_not_change_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        original_request_id = request.request_id

        ExperimentalAdmission(
            admission_id="adm.010",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        ExperimentalAdmission(
            admission_id="adm.011",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            request.request_id,
            original_request_id,
        )

    def test_each_admission_refers_to_same_operation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.012",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.013",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.operation.operation_id,
            second.request.operation.operation_id,
        )

    def test_multiple_admissions_can_exist_without_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.014",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.015",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

        self.assertIsNone(execution_id)

    def test_multiple_admissions_do_not_imply_multiple_executions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.016",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.017",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_ids = []

        admissions = [first, second]

        self.assertEqual(
            len(admissions),
            2,
        )

        self.assertEqual(
            len(execution_ids),
            0,
        )

    def test_admission_count_is_independent_of_execution_count(self):
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
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.019",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        admissions = [first, second]
        executions = ["exec.001"]

        self.assertEqual(
            len(admissions),
            2,
        )

        self.assertEqual(
            len(executions),
            1,
        )

    def test_admission_cardinality_can_be_one_to_many(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admissions = [
            ExperimentalAdmission(
                admission_id="adm.020",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.021",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.022",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        self.assertEqual(
            len(admissions),
            3,
        )

        self.assertTrue(
            all(
                admission.request.request_id == request.request_id
                for admission in admissions
            )
        )

    def test_admission_identity_and_cardinality_are_distinct_concepts(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admissions = [
            ExperimentalAdmission(
                admission_id="adm.023",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.024",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        admission_ids = {
            admission.admission_id
            for admission in admissions
        }

        self.assertEqual(
            len(admission_ids),
            2,
        )

        self.assertEqual(
            len(admissions),
            2,
        )


if __name__ == "__main__":
    unittest.main()