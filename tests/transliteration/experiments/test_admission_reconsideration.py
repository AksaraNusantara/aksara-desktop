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


class TestAdmissionReconsideration(unittest.TestCase):

    def test_reconsideration_preserves_request_identity(self):
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
            second.request.request_id,
        )

    def test_reconsideration_can_change_decision(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.003",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.decision,
            second.decision,
        )

    def test_reconsideration_has_distinct_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.005",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.006",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            first.admission_id,
            second.admission_id,
        )

    def test_first_admission_remains_observable_after_reconsideration(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.007",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.008",
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

    def test_reconsideration_does_not_mutate_first_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.009",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        ExperimentalAdmission(
            admission_id="adm.010",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_reconsideration_does_not_create_new_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.011",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.012",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            first.request.request_id,
            "req.006",
        )

        self.assertEqual(
            second.request.request_id,
            "req.006",
        )

    def test_reconsideration_does_not_require_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.013",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.014",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            first.request.request_id,
            second.request.request_id,
        )

        self.assertIsNone(execution_id)

    def test_reconsideration_can_occur_multiple_times(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        admissions = [
            ExperimentalAdmission(
                admission_id="adm.015",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.016",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.017",
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
                admission.request.request_id == "req.008"
                for admission in admissions
            )
        )

    def test_reconsideration_preserves_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
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

    def test_reconsideration_can_end_with_rejection(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.020",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.021",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            first.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            second.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

    def test_reconsideration_does_not_imply_execution_occurrence(self):
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
                admission_id="adm.022",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.023",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        execution_ids = []

        self.assertEqual(
            len(admissions),
            2,
        )

        self.assertEqual(
            len(execution_ids),
            0,
        )

    def test_reconsideration_can_be_observed_as_a_sequence(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        first = ExperimentalAdmission(
            admission_id="adm.024",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        second = ExperimentalAdmission(
            admission_id="adm.025",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        sequence = [first, second]

        self.assertEqual(
            sequence[0].decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertEqual(
            sequence[1].decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertEqual(
            sequence[0].request.request_id,
            sequence[1].request.request_id,
        )


if __name__ == "__main__":
    unittest.main()