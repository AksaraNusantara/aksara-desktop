import unittest
from enum import Enum


# ============================================================
# Capability State
# ============================================================

class CapabilityState(Enum):

    UNSUPPORTED = "unsupported"

    AVAILABLE = "available"

    UNAVAILABLE = "unavailable"


# ============================================================
# Execution Failure Type
# ============================================================

class FailureType(Enum):

    INVALID_INPUT = "invalid_input"

    EXECUTION_ERROR = "execution_error"


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

        if text == "invalid":

            raise ValueError(
                "Input is not supported"
            )

        if text == "crash":

            raise RuntimeError(
                "Unexpected transliteration failure"
            )

        return (
            f"[Transliterated] {text}"
        )


# ============================================================
# MODEL A
#
# Unified Execution
# ============================================================

class UnifiedCapability:

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

        if not self._available:

            return ExecutionResult(
                success=False,
                failure_type=(
                    "CAPABILITY_UNAVAILABLE"
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

        except ValueError as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType.INVALID_INPUT
                ),
                diagnostic=str(error),
            )

        except Exception as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType.EXECUTION_ERROR
                ),
                diagnostic=str(error),
            )


# ============================================================
# MODEL B
#
# Capability Precondition
# ============================================================

class PreconditionCapability:

    def __init__(
        self,
        state=CapabilityState.AVAILABLE,
    ):

        self._state = state

        self._service = (
            ExperimentalTransliterator()
            if state == CapabilityState.AVAILABLE
            else None
        )

    def get_state(self):

        return self._state

    def execute(
        self,
        text,
    ):

        if self._state != CapabilityState.AVAILABLE:

            raise RuntimeError(
                "Capability is not available "
                "for execution"
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

        except ValueError as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType.INVALID_INPUT
                ),
                diagnostic=str(error),
            )

        except Exception as error:

            return ExecutionResult(
                success=False,
                failure_type=(
                    FailureType.EXECUTION_ERROR
                ),
                diagnostic=str(error),
            )


# ============================================================
# Tests
# ============================================================

class TestPreconditionVsExecutionFailure(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    #
    # Capability unavailable becomes execution result
    # --------------------------------------------------------

    def test_model_a_unavailable_capability(self):

        print("\n" + "=" * 65)
        print(
            "MODEL A: UNIFIED EXECUTION"
        )
        print("=" * 65)

        capability = UnifiedCapability(
            available=False
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            "Caller Action : execute(text)"
        )

        print(
            f"Success       : "
            f"{result.success}"
        )

        print(
            f"Failure Type  : "
            f"{result.failure_type}"
        )

        print(
            f"Diagnostic    : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.failure_type,
            "CAPABILITY_UNAVAILABLE",
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Capability unavailable is precondition state
    # --------------------------------------------------------

    def test_model_b_unavailable_precondition(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: CAPABILITY PRECONDITION"
        )
        print("=" * 65)

        capability = (
            PreconditionCapability(
                state=(
                    CapabilityState.UNAVAILABLE
                )
            )
        )

        state = (
            capability.get_state()
        )

        print(
            "Caller Action : get_state()"
        )

        print(
            f"Capability State : "
            f"{state.name}"
        )

        self.assertEqual(
            state,
            CapabilityState.UNAVAILABLE,
        )

        print(
            "Execution      : NOT ATTEMPTED"
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Successful execution
    # --------------------------------------------------------

    def test_model_b_successful_execution(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: EXECUTION SUCCESS"
        )
        print("=" * 65)

        capability = (
            PreconditionCapability(
                state=(
                    CapabilityState.AVAILABLE
                )
            )
        )

        state = (
            capability.get_state()
        )

        self.assertEqual(
            state,
            CapabilityState.AVAILABLE,
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Capability State : "
            f"{state.name}"
        )

        print(
            f"Success          : "
            f"{result.success}"
        )

        print(
            f"Output           : "
            f"{result.output}"
        )

        self.assertTrue(
            result.success
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Invalid input
    # --------------------------------------------------------

    def test_model_b_invalid_input(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: EXECUTION FAILURE"
        )
        print("=" * 65)

        capability = (
            PreconditionCapability(
                state=(
                    CapabilityState.AVAILABLE
                )
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
            FailureType.INVALID_INPUT,
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Unexpected execution error
    # --------------------------------------------------------

    def test_model_b_execution_error(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: EXECUTION ERROR"
        )
        print("=" * 65)

        capability = (
            PreconditionCapability(
                state=(
                    CapabilityState.AVAILABLE
                )
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
            FailureType.EXECUTION_ERROR,
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )