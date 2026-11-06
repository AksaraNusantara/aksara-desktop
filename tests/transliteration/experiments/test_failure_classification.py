import unittest
from enum import Enum


# ============================================================
# Failure Classification
# ============================================================

class FailureType(Enum):

    CAPABILITY_UNAVAILABLE = (
        "capability_unavailable"
    )

    INVALID_INPUT = (
        "invalid_input"
    )

    EXECUTION_ERROR = (
        "execution_error"
    )


# ============================================================
# Execution Result
# ============================================================

class ExecutionResult:

    def __init__(
        self,
        success,
        output=None,
        failure_type=None,
        diagnostic=None,
    ):

        self.success = success
        self.output = output
        self.failure_type = failure_type
        self.diagnostic = diagnostic


# ============================================================
# Experimental Transliterator
# ============================================================

class ExperimentalTransliterator:

    def transliterate(
        self,
        text,
    ):

        # ----------------------------------------
        # Case B
        # Invalid input
        # ----------------------------------------

        if text == "invalid":

            raise ValueError(
                "Input is not supported"
            )

        # ----------------------------------------
        # Case C
        # Unexpected execution error
        # ----------------------------------------

        if text == "crash":

            raise RuntimeError(
                "Unexpected transliteration failure"
            )

        # ----------------------------------------
        # Successful execution
        # ----------------------------------------

        return (
            f"[Transliterated] {text}"
        )


# ============================================================
# Experimental Capability
# ============================================================

class ExperimentalCapability:

    def __init__(
        self,
        available=True,
    ):

        self._available = available

        self._service = (
            ExperimentalTransliterator()
            if available
            else None
        )

    def execute(
        self,
        text,
    ):

        # ----------------------------------------
        # Case A
        # Capability unavailable
        # ----------------------------------------

        if not self._available:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType
                    .CAPABILITY_UNAVAILABLE
                ),
                diagnostic=(
                    "Transliteration capability "
                    "is not available"
                ),
            )

        try:

            output = (
                self._service
                .transliterate(text)
            )

            return ExecutionResult(
                success=True,
                output=output,
            )

        # ----------------------------------------
        # Case B
        # Input-related failure
        # ----------------------------------------

        except ValueError as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType
                    .INVALID_INPUT
                ),
                diagnostic=str(error),
            )

        # ----------------------------------------
        # Case C
        # Unexpected execution failure
        # ----------------------------------------

        except Exception as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType
                    .EXECUTION_ERROR
                ),
                diagnostic=str(error),
            )


# ============================================================
# Tests
# ============================================================

class TestFailureClassification(
    unittest.TestCase
):

    # --------------------------------------------------------
    # Case A
    # --------------------------------------------------------

    def test_capability_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "CASE A: CAPABILITY UNAVAILABLE"
        )
        print("=" * 65)

        capability = (
            ExperimentalCapability(
                available=False
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Success      : "
            f"{result.success}"
        )

        print(
            f"Failure Type : "
            f"{result.failure_type.name}"
        )

        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.failure_type,
            FailureType
            .CAPABILITY_UNAVAILABLE,
        )


    # --------------------------------------------------------
    # Case B
    # --------------------------------------------------------

    def test_invalid_input(self):

        print("\n" + "=" * 65)
        print(
            "CASE B: INVALID INPUT"
        )
        print("=" * 65)

        capability = (
            ExperimentalCapability(
                available=True
            )
        )

        result = capability.execute(
            "invalid"
        )

        print(
            f"Success      : "
            f"{result.success}"
        )

        print(
            f"Failure Type : "
            f"{result.failure_type.name}"
        )

        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.failure_type,
            FailureType
            .INVALID_INPUT,
        )


    # --------------------------------------------------------
    # Case C
    # --------------------------------------------------------

    def test_execution_error(self):

        print("\n" + "=" * 65)
        print(
            "CASE C: EXECUTION ERROR"
        )
        print("=" * 65)

        capability = (
            ExperimentalCapability(
                available=True
            )
        )

        result = capability.execute(
            "crash"
        )

        print(
            f"Success      : "
            f"{result.success}"
        )

        print(
            f"Failure Type : "
            f"{result.failure_type.name}"
        )

        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.failure_type,
            FailureType
            .EXECUTION_ERROR,
        )


    # --------------------------------------------------------
    # Success Case
    # --------------------------------------------------------

    def test_successful_execution(self):

        print("\n" + "=" * 65)
        print(
            "SUCCESSFUL EXECUTION"
        )
        print("=" * 65)

        capability = (
            ExperimentalCapability(
                available=True
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Success      : "
            f"{result.success}"
        )

        print(
            f"Output       : "
            f"{result.output}"
        )

        print(
            f"Failure Type : "
            f"{result.failure_type}"
        )

        print(
            f"Diagnostic   : "
            f"{result.diagnostic}"
        )

        self.assertTrue(
            result.success
        )

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )

        self.assertIsNone(
            result.failure_type
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )