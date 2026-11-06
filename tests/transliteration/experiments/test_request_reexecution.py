import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()


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


class TestRequestReexecution(unittest.TestCase):

    def test_same_request_can_be_reexecuted(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.001",
            operation=operation,
            input_data="hanacaraka",
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
            request.operation,
            execution_1.operation,
        )

        self.assertEqual(
            request.operation,
            execution_2.operation,
        )

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    def test_reexecution_preserves_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.002.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.002.b",
            operation=operation,
        )

        executions = [execution_1, execution_2]

        self.assertEqual(
            request.request_id,
            "req.002",
        )

        self.assertEqual(
            len(executions),
            2,
        )

    def test_reexecution_has_distinct_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.003.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.003.b",
            operation=operation,
        )

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    def test_reexecution_can_produce_different_results(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.004.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.004.b",
            operation=operation,
        )

        result_1 = ExperimentalExecutionResult(
            execution=execution_1,
            state=ExperimentalExecutionState.FAILED,
        )

        result_2 = ExperimentalExecutionResult(
            execution=execution_2,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            result_1.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            result_2.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_failure_then_success_can_be_represented_as_same_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.005",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.005.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.005.b",
            operation=operation,
        )

        result_1 = ExperimentalExecutionResult(
            execution=execution_1,
            state=ExperimentalExecutionState.FAILED,
        )

        result_2 = ExperimentalExecutionResult(
            execution=execution_2,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            request.operation,
            execution_1.operation,
        )

        self.assertEqual(
            request.operation,
            execution_2.operation,
        )

        self.assertEqual(
            result_1.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            result_2.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_new_request_has_different_request_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_1 = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        request_2 = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertNotEqual(
            request_1.request_id,
            request_2.request_id,
        )

    def test_same_input_does_not_make_requests_identical(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request_1 = ExperimentalExecutionRequest(
            request_id="req.008",
            operation=operation,
            input_data="hanacaraka",
        )

        request_2 = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        self.assertEqual(
            request_1.input_data,
            request_2.input_data,
        )

        self.assertNotEqual(
            request_1.request_id,
            request_2.request_id,
        )

    def test_same_request_can_have_execution_history(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        history = [
            ExperimentalExecutionResult(
                execution=ExperimentalExecution(
                    execution_id="exec.010.a",
                    operation=operation,
                ),
                state=ExperimentalExecutionState.FAILED,
            ),
            ExperimentalExecutionResult(
                execution=ExperimentalExecution(
                    execution_id="exec.010.b",
                    operation=operation,
                ),
                state=ExperimentalExecutionState.SUCCESS,
            ),
        ]

        self.assertEqual(
            len(history),
            2,
        )

        self.assertEqual(
            request.operation,
            history[0].execution.operation,
        )

        self.assertEqual(
            request.operation,
            history[1].execution.operation,
        )

    def test_execution_history_preserves_execution_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        history = [
            ExperimentalExecution(
                execution_id="exec.011.a",
                operation=operation,
            ),
            ExperimentalExecution(
                execution_id="exec.011.b",
                operation=operation,
            ),
        ]

        self.assertNotEqual(
            history[0].execution_id,
            history[1].execution_id,
        )

    def test_retry_semantics_can_be_observed_without_retry_api(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        first_execution = ExperimentalExecution(
            execution_id="exec.012.a",
            operation=operation,
        )

        second_execution = ExperimentalExecution(
            execution_id="exec.012.b",
            operation=operation,
        )

        first_result = ExperimentalExecutionResult(
            execution=first_execution,
            state=ExperimentalExecutionState.FAILED,
        )

        second_result = ExperimentalExecutionResult(
            execution=second_execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            request.operation,
            first_execution.operation,
        )

        self.assertEqual(
            request.operation,
            second_execution.operation,
        )

        self.assertEqual(
            first_result.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            second_result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_reexecution_does_not_change_operation_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.013.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.013.b",
            operation=operation,
        )

        self.assertEqual(
            execution_1.operation.operation_id,
            execution_2.operation.operation_id,
        )

    def test_request_execution_result_chain_can_preserve_all_identities(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.014",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.014.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.014.b",
            operation=operation,
        )

        result_1 = ExperimentalExecutionResult(
            execution=execution_1,
            state=ExperimentalExecutionState.FAILED,
        )

        result_2 = ExperimentalExecutionResult(
            execution=execution_2,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            operation.operation_id,
            "op.transliterate",
        )

        self.assertEqual(
            request.request_id,
            "req.014",
        )

        self.assertEqual(
            result_1.execution.execution_id,
            "exec.014.a",
        )

        self.assertEqual(
            result_2.execution.execution_id,
            "exec.014.b",
        )


if __name__ == "__main__":
    unittest.main()