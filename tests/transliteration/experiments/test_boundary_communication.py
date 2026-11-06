import unittest
from enum import Enum


# ============================================================
# Capability State
# ============================================================

class CapabilityState(Enum):

    AVAILABLE = "available"

    UNAVAILABLE = "unavailable"


# ============================================================
# Experimental Transliterator
# ============================================================

class ExperimentalTransliterator:

    def transliterate(
        self,
        text,
    ):

        return f"[Transliterated] {text}"


# ============================================================
# MODEL A
#
# Boundary Response
# ============================================================

class BoundaryResponse:

    def __init__(
        self,
        executed,
        output=None,
        reason=None,
    ):

        self.executed = executed
        self.output = output
        self.reason = reason


class BoundaryResponseCapability:

    def __init__(
        self,
        state,
    ):

        self._state = state
        self._service = (
            ExperimentalTransliterator()
        )

    def execute(
        self,
        text,
    ):

        if (
            self._state
            != CapabilityState.AVAILABLE
        ):

            return BoundaryResponse(
                executed=False,
                reason=(
                    "Capability is not available"
                ),
            )

        output = (
            self._service
            .transliterate(text)
        )

        return BoundaryResponse(
            executed=True,
            output=output,
        )


# ============================================================
# MODEL B
#
# Controlled Exception
# ============================================================

class CapabilityUnavailableError(Exception):
    pass


class ExceptionCapability:

    def __init__(
        self,
        state,
    ):

        self._state = state
        self._service = (
            ExperimentalTransliterator()
        )

    def execute(
        self,
        text,
    ):

        if (
            self._state
            != CapabilityState.AVAILABLE
        ):

            raise CapabilityUnavailableError(
                "Capability is not available"
            )

        return (
            self._service
            .transliterate(text)
        )


# ============================================================
# MODEL C
#
# Unified Result Object
# ============================================================

class ExecutionState(Enum):

    NOT_EXECUTED = "not_executed"

    SUCCESS = "success"

    FAILED = "failed"


class UnifiedResult:

    def __init__(
        self,
        state,
        output=None,
        reason=None,
    ):

        self.state = state
        self.output = output
        self.reason = reason


class UnifiedResultCapability:

    def __init__(
        self,
        state,
    ):

        self._state = state
        self._service = (
            ExperimentalTransliterator()
        )

    def execute(
        self,
        text,
    ):

        if (
            self._state
            != CapabilityState.AVAILABLE
        ):

            return UnifiedResult(
                state=(
                    ExecutionState.NOT_EXECUTED
                ),
                reason=(
                    "Capability is not available"
                ),
            )

        try:

            output = (
                self._service
                .transliterate(text)
            )

            return UnifiedResult(
                state=(
                    ExecutionState.SUCCESS
                ),
                output=output,
            )

        except Exception as error:

            return UnifiedResult(
                state=(
                    ExecutionState.FAILED
                ),
                reason=str(error),
            )


# ============================================================
# Tests
# ============================================================

class TestBoundaryCommunication(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    #
    # Boundary Response:
    # capability unavailable
    # --------------------------------------------------------

    def test_model_a_boundary_response(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL A: BOUNDARY RESPONSE"
        )
        print("=" * 65)

        capability = (
            BoundaryResponseCapability(
                CapabilityState.UNAVAILABLE
            )
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Executed : "
            f"{result.executed}"
        )

        print(
            f"Output   : "
            f"{result.output}"
        )

        print(
            f"Reason   : "
            f"{result.reason}"
        )

        self.assertFalse(
            result.executed
        )

        self.assertIsNone(
            result.output
        )


    # --------------------------------------------------------
    # MODEL A
    #
    # Boundary Response:
    # execution succeeds
    # --------------------------------------------------------

    def test_model_a_execution_success(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL A: EXECUTION SUCCESS"
        )
        print("=" * 65)

        capability = (
            BoundaryResponseCapability(
                CapabilityState.AVAILABLE
            )
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Executed : "
            f"{result.executed}"
        )

        print(
            f"Output   : "
            f"{result.output}"
        )

        self.assertTrue(
            result.executed
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Controlled Exception:
    # capability unavailable
    # --------------------------------------------------------

    def test_model_b_controlled_exception(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL B: CONTROLLED EXCEPTION"
        )
        print("=" * 65)

        capability = (
            ExceptionCapability(
                CapabilityState.UNAVAILABLE
            )
        )

        with self.assertRaises(
            CapabilityUnavailableError
        ) as context:

            capability.execute(
                "hanacaraka"
            )

        print(
            "Execution : BLOCKED"
        )

        print(
            f"Exception : "
            f"{type(context.exception).__name__}"
        )

        print(
            f"Reason    : "
            f"{context.exception}"
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Controlled Exception:
    # execution succeeds
    # --------------------------------------------------------

    def test_model_b_execution_success(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL B: EXECUTION SUCCESS"
        )
        print("=" * 65)

        capability = (
            ExceptionCapability(
                CapabilityState.AVAILABLE
            )
        )

        output = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            "Execution : COMPLETED"
        )

        print(
            f"Output    : "
            f"{output}"
        )

        self.assertEqual(
            output,
            "[Transliterated] hanacaraka",
        )


    # --------------------------------------------------------
    # MODEL C
    #
    # Unified Result:
    # capability unavailable
    # --------------------------------------------------------

    def test_model_c_not_executed(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL C: UNIFIED RESULT"
        )
        print("=" * 65)

        capability = (
            UnifiedResultCapability(
                CapabilityState.UNAVAILABLE
            )
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"State  : "
            f"{result.state.name}"
        )

        print(
            f"Output : "
            f"{result.output}"
        )

        print(
            f"Reason : "
            f"{result.reason}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.NOT_EXECUTED,
        )


    # --------------------------------------------------------
    # MODEL C
    #
    # Unified Result:
    # execution succeeds
    # --------------------------------------------------------

    def test_model_c_execution_success(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL C: EXECUTION SUCCESS"
        )
        print("=" * 65)

        capability = (
            UnifiedResultCapability(
                CapabilityState.AVAILABLE
            )
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"State  : "
            f"{result.state.name}"
        )

        print(
            f"Output : "
            f"{result.output}"
        )

        self.assertEqual(
            result.state,
            ExecutionState.SUCCESS,
        )

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )