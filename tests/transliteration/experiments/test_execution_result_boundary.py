import unittest
from dataclasses import dataclass
from enum import Enum, auto


class ExperimentalExecutionState(Enum):
    SUCCESS = auto()
    FAILED = auto()
    NOT_EXECUTED = auto()


class ExperimentalFailureClassification(Enum):
    EXECUTION_ERROR = auto()


class ExperimentalNonExecutionReason(Enum):
    CAPABILITY_UNAVAILABLE = auto()
    PRECONDITION_NOT_MET = auto()


# ============================================================
# Model A — Distinct Execution and ExecutionResult
# ============================================================

@dataclass(frozen=True)
class ExperimentalExecution:
    execution_id: str
    operation_id: str


@dataclass(frozen=True)
class ExperimentalExecutionResult:
    execution: ExperimentalExecution
    state: ExperimentalExecutionState
    output: object | None = None
    failure: ExperimentalFailureClassification | None = None
    non_execution_reason: ExperimentalNonExecutionReason | None = None
    diagnostic: str | None = None


# ============================================================
# Model B — Unified ExecutionResult
# ============================================================

@dataclass(frozen=True)
class ExperimentalUnifiedExecutionResult:
    execution_id: str
    operation_id: str
    state: ExperimentalExecutionState
    output: object | None = None
    failure: ExperimentalFailureClassification | None = None
    non_execution_reason: ExperimentalNonExecutionReason | None = None
    diagnostic: str | None = None


class TestExecutionResultBoundary(unittest.TestCase):

    # --------------------------------------------------------
    # 18-5-1
    # --------------------------------------------------------

    def test_distinct_model_can_represent_execution(self):
        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        self.assertEqual(execution.execution_id, "exec.001")
        self.assertEqual(
            execution.operation_id,
            "op.transliterate",
        )

    # --------------------------------------------------------
    # 18-5-2
    # --------------------------------------------------------

    def test_result_can_refer_to_execution(self):
        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertIs(result.execution, execution)
        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    # --------------------------------------------------------
    # 18-5-3
    # --------------------------------------------------------

    def test_same_execution_identity_can_be_observed_through_result(self):
        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.001",
        )

    # --------------------------------------------------------
    # 18-5-4
    # --------------------------------------------------------

    def test_different_executions_can_have_different_results(self):
        execution_1 = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        execution_2 = ExperimentalExecution(
            execution_id="exec.002",
            operation_id="op.transliterate",
        )

        result_1 = ExperimentalExecutionResult(
            execution=execution_1,
            state=ExperimentalExecutionState.SUCCESS,
            output="result-1",
        )

        result_2 = ExperimentalExecutionResult(
            execution=execution_2,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        self.assertNotEqual(
            result_1.execution.execution_id,
            result_2.execution.execution_id,
        )

        self.assertNotEqual(
            result_1.state,
            result_2.state,
        )

    # --------------------------------------------------------
    # 18-5-5
    # --------------------------------------------------------

    def test_execution_identity_is_distinct_from_result_payload(self):
        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.001",
        )

        self.assertEqual(
            result.output,
            "ꦲꦤꦕꦫꦏ",
        )

        self.assertNotEqual(
            execution.execution_id,
            result.output,
        )

    # --------------------------------------------------------
    # 18-5-6
    # --------------------------------------------------------

    def test_unified_model_can_represent_success(self):
        result = ExperimentalUnifiedExecutionResult(
            execution_id="exec.001",
            operation_id="op.transliterate",
            state=ExperimentalExecutionState.SUCCESS,
            output="ꦲꦤꦕꦫꦏ",
        )

        self.assertEqual(
            result.execution_id,
            "exec.001",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.SUCCESS,
        )

    # --------------------------------------------------------
    # 18-5-7
    # --------------------------------------------------------

    def test_unified_model_can_represent_failure(self):
        result = ExperimentalUnifiedExecutionResult(
            execution_id="exec.002",
            operation_id="op.transliterate",
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.FAILED,
        )

        self.assertEqual(
            result.failure,
            ExperimentalFailureClassification.EXECUTION_ERROR,
        )

    # --------------------------------------------------------
    # 18-5-8
    # --------------------------------------------------------

    def test_unified_model_can_represent_non_execution(self):
        result = ExperimentalUnifiedExecutionResult(
            execution_id="exec.003",
            operation_id="op.transliterate",
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.PRECONDITION_NOT_MET
            ),
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.PRECONDITION_NOT_MET,
        )

    # --------------------------------------------------------
    # 18-5-9
    # --------------------------------------------------------

    def test_distinct_and_unified_models_can_express_same_success_semantics(self):
        execution = ExperimentalExecution(
            execution_id="exec.001",
            operation_id="op.transliterate",
        )

        distinct = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.SUCCESS,
            output="result",
        )

        unified = ExperimentalUnifiedExecutionResult(
            execution_id="exec.001",
            operation_id="op.transliterate",
            state=ExperimentalExecutionState.SUCCESS,
            output="result",
        )

        self.assertEqual(
            distinct.execution.execution_id,
            unified.execution_id,
        )

        self.assertEqual(
            distinct.execution.operation_id,
            unified.operation_id,
        )

        self.assertEqual(
            distinct.state,
            unified.state,
        )

        self.assertEqual(
            distinct.output,
            unified.output,
        )

    # --------------------------------------------------------
    # 18-5-10
    # --------------------------------------------------------

    def test_distinct_and_unified_models_can_express_same_failure_semantics(self):
        execution = ExperimentalExecution(
            execution_id="exec.002",
            operation_id="op.transliterate",
        )

        distinct = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        unified = ExperimentalUnifiedExecutionResult(
            execution_id="exec.002",
            operation_id="op.transliterate",
            state=ExperimentalExecutionState.FAILED,
            failure=ExperimentalFailureClassification.EXECUTION_ERROR,
        )

        self.assertEqual(
            distinct.execution.execution_id,
            unified.execution_id,
        )

        self.assertEqual(
            distinct.state,
            unified.state,
        )

        self.assertEqual(
            distinct.failure,
            unified.failure,
        )

    # --------------------------------------------------------
    # 18-5-11
    # --------------------------------------------------------

    def test_execution_identity_can_exist_without_result_in_distinct_model(self):
        execution = ExperimentalExecution(
            execution_id="exec.004",
            operation_id="op.transliterate",
        )

        self.assertEqual(
            execution.execution_id,
            "exec.004",
        )

        self.assertEqual(
            execution.operation_id,
            "op.transliterate",
        )

    # --------------------------------------------------------
    # 18-5-12
    # --------------------------------------------------------

    def test_result_contains_observable_execution_semantics(self):
        execution = ExperimentalExecution(
            execution_id="exec.005",
            operation_id="op.transliterate",
        )

        result = ExperimentalExecutionResult(
            execution=execution,
            state=ExperimentalExecutionState.NOT_EXECUTED,
            non_execution_reason=(
                ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE
            ),
            diagnostic="Capability unavailable.",
        )

        self.assertEqual(
            result.execution.execution_id,
            "exec.005",
        )

        self.assertEqual(
            result.state,
            ExperimentalExecutionState.NOT_EXECUTED,
        )

        self.assertEqual(
            result.non_execution_reason,
            ExperimentalNonExecutionReason.CAPABILITY_UNAVAILABLE,
        )

        self.assertEqual(
            result.diagnostic,
            "Capability unavailable.",
        )


if __name__ == "__main__":
    unittest.main()