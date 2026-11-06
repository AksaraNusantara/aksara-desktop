import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalNonExecutionReason(Enum):
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
    non_execution_reason: (
        ExperimentalNonExecutionReason | None
    ) = None


class TestRequestCancellationBoundary(unittest.TestCase):

    # --------------------------------------------------------
    # 19-5-1
    # --------------------------------------------------------

    def test_request_can_be_cancelled_before_execution(self):
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
    # 19-5-2
    # --------------------------------------------------------

    def test_cancelled_before_execution_has_no_execution_identity(self):
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

    # --------------------------------------------------------
    # 19-5-3
    # --------------------------------------------------------

    def test_pre_execution_cancellation_is_not_execution_failure(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # 19-5-4
    # --------------------------------------------------------

    def test_pre_execution_cancellation_has_non_execution_reason(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.REQUEST_CANCELLED,
        )

    # --------------------------------------------------------
    # 19-5-5
    # --------------------------------------------------------

    def test_execution_can_exist_before_cancellation_result(self):
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
        )

        self.assertIsNotNone(
            result.execution
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.001",
        )

    # --------------------------------------------------------
    # 19-5-6
    # --------------------------------------------------------

    def test_post_start_cancellation_does_not_require_not_executed(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.002",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
        )

        self.assertIsNotNone(
            result.execution
        )

        self.assertNotEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # 19-5-7
    # --------------------------------------------------------

    def test_request_identity_exists_independently_of_execution_state(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.003",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            request.request_id,
            "req.003",
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.003",
        )

    # --------------------------------------------------------
    # 19-5-8
    # --------------------------------------------------------

    def test_same_operation_can_have_cancelled_and_executed_requests(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_1 = ExperimentalExecutionRequest(
            request_id="req.004",
            operation=operation,
            input_data="hanacaraka",
        )

        request_2 = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        cancelled_result = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation=operation,
        )

        executed_result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            request_1.operation,
            request_2.operation,
        )

        self.assertIsNone(
            cancelled_result.execution
        )

        self.assertIsNotNone(
            executed_result.execution
        )

    # --------------------------------------------------------
    # 19-5-9
    # --------------------------------------------------------

    def test_cancellation_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
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
            "op.transliterate",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

    # --------------------------------------------------------
    # 19-5-10
    # --------------------------------------------------------

    def test_pre_execution_cancellation_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
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
            "req.007",
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.REQUEST_CANCELLED,
        )

    # --------------------------------------------------------
    # 19-5-11
    # --------------------------------------------------------

    def test_execution_identity_is_evidence_that_execution_started(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution = ExperimentalExecution(
            execution_id="exec.008",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
        )

        self.assertIsNotNone(
            result.execution
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.008",
        )

    # --------------------------------------------------------
    # 19-5-12
    # --------------------------------------------------------

    def test_request_lifecycle_and_execution_lifecycle_can_be_distinguished(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        cancelled_before_start = ExperimentalExecutionResult(
            execution=None,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.REQUEST_CANCELLED
            ),
        )

        execution = ExperimentalExecution(
            execution_id="exec.009",
            operation=operation,
        )

        cancelled_after_start = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            request.request_id,
            "req.009",
        )

        self.assertIsNone(
            cancelled_before_start.execution
        )

        self.assertIsNotNone(
            cancelled_after_start.execution
        )

        self.assertEqual(
            cancelled_before_start.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertNotEqual(
            cancelled_after_start.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )


if __name__ == "__main__":
    unittest.main()