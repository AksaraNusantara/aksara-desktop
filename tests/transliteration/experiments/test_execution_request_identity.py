import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


# ============================================================
# Experimental Identity Models
# ============================================================

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
    execution: ExperimentalExecution
    state: ExperimentalExecutionState
    output: object | None = None


class TestExecutionRequestIdentity(unittest.TestCase):

    # --------------------------------------------------------
    # 19-1-1
    # --------------------------------------------------------

    def test_request_has_independent_identity(self):
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

    # --------------------------------------------------------
    # 19-1-2
    # --------------------------------------------------------

    def test_request_identity_is_not_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertNotEqual(
            request.request_id,
            request.operation.operation_id,
        )

    # --------------------------------------------------------
    # 19-1-3
    # --------------------------------------------------------

    def test_execution_has_independent_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation=operation,
        )

        self.assertEqual(
            execution.execution_id,
            "exec.001",
        )

    # --------------------------------------------------------
    # 19-1-4
    # --------------------------------------------------------

    def test_request_and_execution_can_have_distinct_identity(self):
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

        self.assertNotEqual(
            request.request_id,
            execution.execution_id,
        )

    # --------------------------------------------------------
    # 19-1-5
    # --------------------------------------------------------

    def test_request_can_describe_operation_input(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
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
    # 19-1-6
    # --------------------------------------------------------

    def test_execution_can_exist_without_request_reference(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation=operation,
        )

        self.assertEqual(
            execution.operation.operation_id,
            "op.transliterate",
        )

        self.assertIsNotNone(
            execution.execution_id
        )

    # --------------------------------------------------------
    # 19-1-7
    # --------------------------------------------------------

    def test_multiple_requests_can_target_same_operation(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_1 = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
        )

        request_2 = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="aksara",
        )

        self.assertEqual(
            request_1.operation,
            request_2.operation,
        )

        self.assertNotEqual(
            request_1.request_id,
            request_2.request_id,
        )

    # --------------------------------------------------------
    # 19-1-8
    # --------------------------------------------------------

    def test_same_operation_can_have_multiple_execution_occurrences(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.001",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.002",
            operation=operation,
        )

        self.assertEqual(
            execution_1.operation,
            execution_2.operation,
        )

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    # --------------------------------------------------------
    # 19-1-9
    # --------------------------------------------------------

    def test_request_and_execution_can_share_operation_identity(self):
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
    # 19-1-10
    # --------------------------------------------------------

    def test_execution_result_identifies_execution_not_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.001",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    # --------------------------------------------------------
    # 19-1-11
    # --------------------------------------------------------

    def test_request_identity_can_remain_distinct_from_result_identity(self):
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

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertNotEqual(
            request.request_id,
            result.execution.execution_id,
        )

    # --------------------------------------------------------
    # 19-1-12
    # --------------------------------------------------------

    def test_identity_levels_form_distinct_conceptual_chain(self):
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

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            operation.operation_id,
            "op.transliterate",
        )

        self.assertEqual(
            request.request_id,
            "req.001",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.001",
        )

        self.assertEqual(
            result.execution.execution_id,
            execution.execution_id,
        )

        self.assertNotEqual(
            operation.operation_id,
            request.request_id,
        )

        self.assertNotEqual(
            request.request_id,
            execution.execution_id,
        )


if __name__ == "__main__":
    unittest.main()