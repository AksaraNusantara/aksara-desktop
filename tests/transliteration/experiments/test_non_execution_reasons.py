import unittest
from enum import Enum


# ============================================================
# EXECUTION STATE
# ============================================================

class ExecutionState(Enum):

    NOT_EXECUTED = "not_executed"
    SUCCESS = "success"
    FAILED = "failed"


# ============================================================
# NON-EXECUTION REASON
# ============================================================

class NonExecutionReason(Enum):

    CAPABILITY_UNAVAILABLE = "capability_unavailable"
    PRECONDITION_NOT_MET = "precondition_not_met"
    EXECUTION_BLOCKED = "execution_blocked"
    REQUEST_CANCELLED = "request_cancelled"


# ============================================================
# FAILURE CLASSIFICATION
# ============================================================

class FailureClassification(Enum):

    INVALID_INPUT = "invalid_input"
    EXECUTION_ERROR = "execution_error"


# ============================================================
# EXECUTION RESULT
# ============================================================

class ExecutionResult:

    def __init__(
        self,
        state,
        output=None,
        non_execution_reason=None,
        failure=None,
        diagnostic=None
    ):
        self.state = state
        self.output = output
        self.non_execution_reason = non_execution_reason
        self.failure = failure
        self.diagnostic = diagnostic


# ============================================================
# EXPERIMENTAL EXECUTOR
# ============================================================

class ExperimentalExecutor:

    def __init__(
        self,
        capability_available=True,
        execution_mode="success"
    ):
        self.capability_available = capability_available
        self.execution_mode = execution_mode

    def execute(self, text):

        # ----------------------------------------------------
        # CAPABILITY UNAVAILABLE
        # ----------------------------------------------------

        if self.execution_mode == "capability_unavailable":

            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.CAPABILITY_UNAVAILABLE
                ),
                diagnostic="Transliteration capability is not available"
            )

        # ----------------------------------------------------
        # PRECONDITION NOT MET
        # ----------------------------------------------------

        if self.execution_mode == "precondition_not_met":

            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.PRECONDITION_NOT_MET
                ),
                diagnostic="Required precondition is not satisfied"
            )

        # ----------------------------------------------------
        # EXECUTION BLOCKED
        # ----------------------------------------------------

        if self.execution_mode == "execution_blocked":

            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.EXECUTION_BLOCKED
                ),
                diagnostic="Execution was blocked before it started"
            )

        # ----------------------------------------------------
        # REQUEST CANCELLED
        # ----------------------------------------------------

        if self.execution_mode == "request_cancelled":

            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                non_execution_reason=(
                    NonExecutionReason.REQUEST_CANCELLED
                ),
                diagnostic="Request was cancelled before execution"
            )

        # ----------------------------------------------------
        # INVALID INPUT
        # ----------------------------------------------------

        if self.execution_mode == "invalid_input":

            return ExecutionResult(
                state=ExecutionState.FAILED,
                failure=FailureClassification.INVALID_INPUT,
                diagnostic="Input is not supported"
            )

        # ----------------------------------------------------
        # EXECUTION ERROR
        # ----------------------------------------------------

        if self.execution_mode == "execution_error":

            return ExecutionResult(
                state=ExecutionState.FAILED,
                failure=FailureClassification.EXECUTION_ERROR,
                diagnostic="Unexpected transliteration failure"
            )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        return ExecutionResult(
            state=ExecutionState.SUCCESS,
            output=f"[Transliterated] {text}"
        )


# ============================================================
# TESTS
# ============================================================

class TestNonExecutionReasons(unittest.TestCase):


    # ========================================================
    # CASE A
    # CAPABILITY UNAVAILABLE
    # ========================================================

    def test_capability_unavailable(self):

        print("\n" + "=" * 65)
        print("CASE A: CAPABILITY UNAVAILABLE")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="capability_unavailable"
        )

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(
            f"Non-Execution Reason: "
            f"{result.non_execution_reason.name}"
        )
        print(f"Failure             : {result.failure}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.CAPABILITY_UNAVAILABLE
        )

        self.assertIsNone(result.failure)
        self.assertIsNone(result.output)


    # ========================================================
    # CASE B
    # PRECONDITION NOT MET
    # ========================================================

    def test_precondition_not_met(self):

        print("\n" + "=" * 65)
        print("CASE B: PRECONDITION NOT MET")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="precondition_not_met"
        )

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(
            f"Non-Execution Reason: "
            f"{result.non_execution_reason.name}"
        )
        print(f"Failure             : {result.failure}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.PRECONDITION_NOT_MET
        )

        self.assertIsNone(result.failure)
        self.assertIsNone(result.output)


    # ========================================================
    # CASE C
    # EXECUTION BLOCKED
    # ========================================================

    def test_execution_blocked(self):

        print("\n" + "=" * 65)
        print("CASE C: EXECUTION BLOCKED")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="execution_blocked"
        )

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(
            f"Non-Execution Reason: "
            f"{result.non_execution_reason.name}"
        )
        print(f"Failure             : {result.failure}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.EXECUTION_BLOCKED
        )

        self.assertIsNone(result.failure)
        self.assertIsNone(result.output)


    # ========================================================
    # CASE D
    # REQUEST CANCELLED
    # ========================================================

    def test_request_cancelled(self):

        print("\n" + "=" * 65)
        print("CASE D: REQUEST CANCELLED")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="request_cancelled"
        )

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(
            f"Non-Execution Reason: "
            f"{result.non_execution_reason.name}"
        )
        print(f"Failure             : {result.failure}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED
        )

        self.assertEqual(
            result.non_execution_reason,
            NonExecutionReason.REQUEST_CANCELLED
        )

        self.assertIsNone(result.failure)
        self.assertIsNone(result.output)


    # ========================================================
    # CASE E
    # SUCCESS CONTROL
    # ========================================================

    def test_success_control(self):

        print("\n" + "=" * 65)
        print("CASE E: SUCCESS CONTROL")
        print("=" * 65)

        executor = ExperimentalExecutor()

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(f"Non-Execution Reason: {result.non_execution_reason}")
        print(f"Failure             : {result.failure}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.SUCCESS
        )

        self.assertIsNone(result.non_execution_reason)
        self.assertIsNone(result.failure)

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka"
        )


    # ========================================================
    # CASE F
    # FAILED CONTROL
    # ========================================================

    def test_failed_control(self):

        print("\n" + "=" * 65)
        print("CASE F: FAILED CONTROL")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="execution_error"
        )

        result = executor.execute("hanacaraka")

        print(f"State               : {result.state.name}")
        print(f"Non-Execution Reason: {result.non_execution_reason}")
        print(f"Failure             : {result.failure.name}")
        print(f"Output              : {result.output}")
        print(
            f"Diagnostic          : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.FAILED
        )

        self.assertIsNone(result.non_execution_reason)

        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR
        )

        self.assertIsNone(result.output)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )