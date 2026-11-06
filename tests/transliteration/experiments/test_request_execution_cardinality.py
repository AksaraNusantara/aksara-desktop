import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


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


class TestRequestExecutionCardinality(unittest.TestCase):

    def test_one_request_can_have_one_execution(self):
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

    def test_request_and_execution_have_distinct_identity(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.002",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.002",
            operation=operation,
        )

        self.assertNotEqual(
            request.request_id,
            execution.execution_id,
        )

    def test_one_request_can_be_associated_with_multiple_executions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.003",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.003.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.003.b",
            operation=operation,
        )

        executions = [execution_1, execution_2]

        self.assertEqual(len(executions), 2)

        self.assertEqual(
            request.operation,
            execution_1.operation,
        )

        self.assertEqual(
            request.operation,
            execution_2.operation,
        )

    def test_multiple_executions_have_distinct_identity(self):
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

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    def test_multiple_executions_can_have_different_results(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
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
            result_1.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            result_2.state,
            ExperimentalExecutionState.SUCCESS,
        )

    def test_request_identity_can_remain_constant_across_executions(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.006",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.006.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.006.b",
            operation=operation,
        )

        self.assertEqual(
            request.request_id,
            "req.006",
        )

        self.assertNotEqual(
            execution_1.execution_id,
            execution_2.execution_id,
        )

    def test_execution_count_can_exceed_one_for_same_request(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.007",
            operation=operation,
            input_data="hanacaraka",
        )

        executions = [
            ExperimentalExecution(
                execution_id="exec.007.a",
                operation=operation,
            ),
            ExperimentalExecution(
                execution_id="exec.007.b",
                operation=operation,
            ),
        ]

        self.assertGreater(
            len(executions),
            1,
        )

        self.assertEqual(
            request.operation,
            executions[0].operation,
        )

    def test_each_execution_can_have_its_own_result(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.008.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.008.b",
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

        self.assertNotEqual(
            result_1.execution.execution_id,
            result_2.execution.execution_id,
        )

    def test_request_does_not_change_when_execution_occurrences_change(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.009",
            operation=operation,
            input_data="hanacaraka",
        )

        execution_1 = ExperimentalExecution(
            execution_id="exec.009.a",
            operation=operation,
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.009.b",
            operation=operation,
        )

        self.assertEqual(
            request.input_data,
            "hanacaraka",
        )

        self.assertEqual(
            request.operation,
            execution_1.operation,
        )

        self.assertEqual(
            request.operation,
            execution_2.operation,
        )

    def test_cardinality_can_be_one_to_many(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.010",
            operation=operation,
            input_data="hanacaraka",
        )

        executions = [
            ExperimentalExecution(
                execution_id="exec.010.a",
                operation=operation,
            ),
            ExperimentalExecution(
                execution_id="exec.010.b",
                operation=operation,
            ),
            ExperimentalExecution(
                execution_id="exec.010.c",
                operation=operation,
            ),
        ]

        self.assertEqual(
            len(executions),
            3,
        )

        self.assertTrue(
            all(
                execution.operation == request.operation
                for execution in executions
            )
        )

    def test_one_to_many_does_not_require_multiple_requests(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.011",
            operation=operation,
            input_data="hanacaraka",
        )

        executions = [
            ExperimentalExecution(
                execution_id="exec.011.a",
                operation=operation,
            ),
            ExperimentalExecution(
                execution_id="exec.011.b",
                operation=operation,
            ),
        ]

        self.assertEqual(
            request.request_id,
            "req.011",
        )

        self.assertEqual(
            len(executions),
            2,
        )

    def test_request_execution_result_chain_can_be_represented(self):
        operation = ExperimentalOperation(
            operation_id="op.transliterate"
        )

        request = ExperimentalExecutionRequest(
            request_id="req.012",
            operation=operation,
            input_data="hanacaraka",
        )

        execution = ExperimentalExecution(
            execution_id="exec.012",
            operation=operation,
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
        )

        self.assertEqual(
            request.operation,
            execution.operation,
        )

        self.assertEqual(
            result.execution,
            execution,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )


if __name__ == "__main__":
    unittest.main()