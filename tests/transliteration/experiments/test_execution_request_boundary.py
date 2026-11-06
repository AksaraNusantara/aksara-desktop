import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalNonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = auto()
    PRECONDITION_NOT_MET = auto()
    REQUEST_CANCELLED = auto()


@dataclass(frozen=True)
class ExperimentalOperation:
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionRequest:
    request_id: str
    operation: ExperimentalOperation
    input_data: object


@dataclass(frozen=True)
class ExperimentalExecution:
    execution_id: str
    operation: ExperimentalOperation


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    execution: ExperimentalExecution | None
    state: ExperimentalExecutionState
    output: object | None = None
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


class TestExecutionRequestBoundary(unittest.TestCase):

    # --------------------------------------------------------
    # 19-2-1
    # --------------------------------------------------------

    def test_request_has_meaning_before_execution(self):
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

        self.assertEqual(
            request.operation.operation_id,
            "op.transliterate",
        )

        self.assertEqual(
            request.input_data,
            "hanacaraka",
        )

    # --------------------------------------------------------
    # 19-2-2
    # --------------------------------------------------------

    def test_request_does_not_require_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertIsNone(
            getattr(request, "execution_id", None)
        )

    # --------------------------------------------------------
    # 19-2-3
    # --------------------------------------------------------

    def test_request_can_be_followed_by_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation=operation,
        )

        self.assertEqual(
            request.operation.operation_id,
            execution.operation.operation_id,
        )

    # --------------------------------------------------------
    # 19-2-4
    # --------------------------------------------------------

    def test_request_can_end_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        self.assertEqual(
            request.request_id,
            "req.002",
        )

        self.assertIsNone(
            result.execution
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # 19-2-5
    # --------------------------------------------------------

    def test_capability_unavailable_request_need_not_create_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
            ),
        )

        self.assertEqual(
            request.request_id,
            "req.003",
        )

        self.assertIsNone(
            result.execution
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
        )

    # --------------------------------------------------------
    # 19-2-6
    # --------------------------------------------------------

    def test_precondition_failure_can_occur_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            request.input_data,
            "",
        )

        self.assertIsNone(
            result.execution
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # 19-2-7
    # --------------------------------------------------------

    def test_successful_execution_produces_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            request.operation.operation_id,
            execution.operation.operation_id,
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.005",
        )

    # --------------------------------------------------------
    # 19-2-8
    # --------------------------------------------------------

    def test_request_identity_survives_independently_of_execution_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.006",
            operation=operation,
        )

        success_result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            request.request_id,
            "req.006",
        )

        self.assertEqual(
            success_result.execution.execution_id,
            "exec.006",
        )

    # --------------------------------------------------------
    # 19-2-9
    # --------------------------------------------------------

    def test_request_and_execution_have_different_semantic_roles(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.007",
            operation=operation,
        )

        self.assertEqual(
            request.input_data,
            "hanacaraka",
        )

        self.assertEqual(
            execution.operation.operation_id,
            "op.transliterate",
        )

        self.assertNotEqual(
            request.request_id,
            execution.execution_id,
        )

    # --------------------------------------------------------
    # 19-2-10
    # --------------------------------------------------------

    def test_not_executed_result_can_be_associated_with_request_semantically(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        self.assertEqual(
            request.operation.operation_id,
            operation.operation_id,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertIsNone(
            result.execution
        )

    # --------------------------------------------------------
    # 19-2-11
    # --------------------------------------------------------

    def test_execution_is_an_occurrence_not_a_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.009",
            operation=operation,
        )

        self.assertEqual(
            request.operation,
            execution.operation,
        )

        self.assertNotEqual(
            request.request_id,
            execution.execution_id,
        )

    # --------------------------------------------------------
    # 19-2-12
    # --------------------------------------------------------

    def test_boundary_model_can_represent_request_without_execution(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        self.assertIsNotNone(request)
        self.assertIsNone(result.execution)

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )


if __name__ == "__main__":
    unittest.main()