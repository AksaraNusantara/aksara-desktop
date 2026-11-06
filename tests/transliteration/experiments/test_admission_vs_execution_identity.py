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


@dataclass(frozen=True)
class ExperimentalExecution:
    execution_id: str
    request: ExperimentalExecutionRequest


class TestAdmissionVsExecutionIdentity(unittest.TestCase):

    def test_admission_can_exist_without_execution(self):
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
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution = None

        self.assertEqual(
            admission.admission_id,
            "adm.001",
        )

        self.assertIsNone(execution)

    def test_execution_has_identity_distinct_from_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.002",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.001",
            request=request,
        )

        self.assertNotEqual(
            admission.admission_id,
            execution.execution_id,
        )

    def test_admission_and_execution_preserve_same_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.003",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.002",
            request=request,
        )

        self.assertEqual(
            admission.request.request_id,
            execution.request.request_id,
        )

    def test_admission_identity_does_not_become_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.004",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.003",
            request=request,
        )

        self.assertNotEqual(
            admission.admission_id,
            execution.execution_id,
        )

    def test_execution_identity_does_not_change_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.005",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        original_admission_id = admission.admission_id

        ExperimentalExecution(
            execution_id="exec.004",
            request=request,
        )

        self.assertEqual(
            admission.admission_id,
            original_admission_id,
        )

    def test_multiple_executions_can_follow_one_admission(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.006",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        executions = [
            ExperimentalExecution(
                execution_id="exec.005",
                request=request,
            ),
            ExperimentalExecution(
                execution_id="exec.006",
                request=request,
            ),
        ]

        self.assertEqual(
            len(executions),
            2,
        )

        self.assertEqual(
            admission.request.request_id,
            executions[0].request.request_id,
        )

        self.assertEqual(
            admission.request.request_id,
            executions[1].request.request_id,
        )

    def test_multiple_admissions_can_exist_without_execution(self):
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
                admission_id="adm.007",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.008",
                request=request,
                decision=ExperimentalAdmissionDecision.REJECTED,
            ),
        ]

        executions = []

        self.assertEqual(
            len(admissions),
            2,
        )

        self.assertEqual(
            len(executions),
            0,
        )

    def test_admission_count_and_execution_count_are_independent(self):
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
                admission_id="adm.009",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
            ExperimentalAdmission(
                admission_id="adm.010",
                request=request,
                decision=ExperimentalAdmissionDecision.ACCEPTED,
            ),
        ]

        executions = [
            ExperimentalExecution(
                execution_id="exec.007",
                request=request,
            ),
        ]

        self.assertEqual(
            len(admissions),
            2,
        )

        self.assertEqual(
            len(executions),
            1,
        )

    def test_rejected_admission_has_no_required_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.011",
            request=request,
            decision=ExperimentalAdmissionDecision.REJECTED,
        )

        execution_id = None

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.REJECTED,
        )

        self.assertIsNone(execution_id)

    def test_accepted_admission_and_execution_have_distinct_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.012",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.008",
            request=request,
        )

        self.assertEqual(
            admission.decision,
            ExperimentalAdmissionDecision.ACCEPTED,
        )

        self.assertNotEqual(
            admission.admission_id,
            execution.execution_id,
        )

    def test_execution_identity_can_be_created_after_admission_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.013",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution_id = None

        self.assertEqual(
            admission.admission_id,
            "adm.013",
        )

        self.assertIsNone(execution_id)

        execution = ExperimentalExecution(
            execution_id="exec.009",
            request=request,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.009",
        )

        self.assertNotEqual(
            admission.admission_id,
            execution.execution_id,
        )

    def test_admission_and_execution_are_distinct_occurrences(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        admission = ExperimentalAdmission(
            admission_id="adm.014",
            request=request,
            decision=ExperimentalAdmissionDecision.ACCEPTED,
        )

        execution = ExperimentalExecution(
            execution_id="exec.010",
            request=request,
        )

        self.assertNotEqual(
            admission.admission_id,
            execution.execution_id,
        )

        self.assertEqual(
            admission.request.request_id,
            execution.request.request_id,
        )


if __name__ == "__main__":
    unittest.main()