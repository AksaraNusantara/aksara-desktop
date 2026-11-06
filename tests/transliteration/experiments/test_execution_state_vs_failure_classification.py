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
# FAILURE CLASSIFICATION
# ============================================================

class FailureClassification(Enum):

    CAPABILITY_UNAVAILABLE = "capability_unavailable"
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
        failure=None,
        diagnostic=None
    ):
        self.state = state
        self.output = output
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
        # CAPABILITY BOUNDARY
        # ----------------------------------------------------

        if not self.capability_available:

            return ExecutionResult(
                state=ExecutionState.NOT_EXECUTED,
                failure=FailureClassification.CAPABILITY_UNAVAILABLE,
                diagnostic="Transliteration capability is not available"
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

class TestExecutionStateVsFailureClassification(unittest.TestCase):


    # ========================================================
    # CASE A
    # CAPABILITY UNAVAILABLE
    # ========================================================

    def test_capability_unavailable(self):

        print("\n" + "=" * 65)
        print("CASE A: CAPABILITY UNAVAILABLE")
        print("=" * 65)

        executor = ExperimentalExecutor(
            capability_available=False
        )

        result = executor.execute("hanacaraka")

        print(f"State        : {result.state.name}")
        print(
            f"Failure      : "
            f"{result.failure.name}"
        )
        print(f"Output       : {result.output}")
        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED
        )

        self.assertEqual(
            result.failure,
            FailureClassification.CAPABILITY_UNAVAILABLE
        )

        self.assertIsNone(result.output)


    # ========================================================
    # CASE B
    # INVALID INPUT
    # ========================================================

    def test_invalid_input(self):

        print("\n" + "=" * 65)
        print("CASE B: INVALID INPUT")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="invalid_input"
        )

        result = executor.execute("hanacaraka")

        print(f"State        : {result.state.name}")
        print(
            f"Failure      : "
            f"{result.failure.name}"
        )
        print(f"Output       : {result.output}")
        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.FAILED
        )

        self.assertEqual(
            result.failure,
            FailureClassification.INVALID_INPUT
        )

        self.assertIsNone(result.output)


    # ========================================================
    # CASE C
    # EXECUTION ERROR
    # ========================================================

    def test_execution_error(self):

        print("\n" + "=" * 65)
        print("CASE C: EXECUTION ERROR")
        print("=" * 65)

        executor = ExperimentalExecutor(
            execution_mode="execution_error"
        )

        result = executor.execute("hanacaraka")

        print(f"State        : {result.state.name}")
        print(
            f"Failure      : "
            f"{result.failure.name}"
        )
        print(f"Output       : {result.output}")
        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.FAILED
        )

        self.assertEqual(
            result.failure,
            FailureClassification.EXECUTION_ERROR
        )

        self.assertIsNone(result.output)


    # ========================================================
    # CASE D
    # SUCCESS
    # ========================================================

    def test_success(self):

        print("\n" + "=" * 65)
        print("CASE D: SUCCESS")
        print("=" * 65)

        executor = ExperimentalExecutor()

        result = executor.execute("hanacaraka")

        print(f"State        : {result.state.name}")
        print(
            f"Failure      : "
            f"{result.failure}"
        )
        print(f"Output       : {result.output}")
        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.SUCCESS
        )

        self.assertIsNone(result.failure)

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )