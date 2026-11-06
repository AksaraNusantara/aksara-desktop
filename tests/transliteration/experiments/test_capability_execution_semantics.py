import unittest
from enum import Enum


# ============================================================
# Capability State
# ============================================================

class CapabilityState(Enum):

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


# ============================================================
# Capability Status
# ============================================================

class CapabilityStatus:

    def __init__(
        self,
        state,
        reason=None,
    ):
        self.state = state
        self.reason = reason

    def is_available(self):

        return (
            self.state
            == CapabilityState.AVAILABLE
        )


# ============================================================
# Experimental Service
# ============================================================

class ExperimentalTransliterator:

    def transliterate(
        self,
        text,
    ):

        if text == "unsupported":

            raise ValueError(
                "Unsupported input"
            )

        return (
            f"[Transliterated] {text}"
        )


# ============================================================
# MODEL 1
# None-based execution semantics
# ============================================================

class NoneResultCapability:

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

    def get_status(self):

        if self._available:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Transliteration service "
                "is not available"
            ),
        )

    def execute(
        self,
        text,
    ):

        if not self.get_status().is_available():

            return None

        try:

            return (
                self._service
                .transliterate(text)
            )

        except ValueError:

            return None


# ============================================================
# Execution Result
# ============================================================

class ExecutionResult:

    def __init__(
        self,
        success,
        output=None,
        diagnostic=None,
    ):

        self.success = success
        self.output = output
        self.diagnostic = diagnostic


# ============================================================
# MODEL 2
# Structured execution semantics
# ============================================================

class StructuredResultCapability:

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

    def get_status(self):

        if self._available:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Transliteration service "
                "is not available"
            ),
        )

    def execute(
        self,
        text,
    ):

        status = self.get_status()

        # ----------------------------------------------------
        # Case A
        # Capability unavailable
        # ----------------------------------------------------

        if not status.is_available():

            return ExecutionResult(
                success=False,
                diagnostic=status.reason,
            )

        try:

            # ------------------------------------------------
            # Case B
            # Execution successful
            # ------------------------------------------------

            output = (
                self._service
                .transliterate(text)
            )

            return ExecutionResult(
                success=True,
                output=output,
            )

        except ValueError as error:

            # ------------------------------------------------
            # Case C
            # Execution failed
            # ------------------------------------------------

            return ExecutionResult(
                success=False,
                diagnostic=str(error),
            )


# ============================================================
# Tests
# ============================================================

class TestCapabilityExecutionSemantics(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL 1
    # --------------------------------------------------------

    def test_none_result_success(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 1: NONE RESULT "
            "(SUCCESS)"
        )
        print("=" * 65)

        capability = (
            NoneResultCapability(
                available=True
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Result : {result}"
        )

        self.assertEqual(
            result,
            "[Transliterated] hanacaraka",
        )


    def test_none_result_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 1: NONE RESULT "
            "(CAPABILITY UNAVAILABLE)"
        )
        print("=" * 65)

        capability = (
            NoneResultCapability(
                available=False
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Result : {result}"
        )

        print(
            "Meaning: UNKNOWN"
        )

        self.assertIsNone(
            result
        )


    def test_none_result_execution_failure(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 1: NONE RESULT "
            "(EXECUTION FAILURE)"
        )
        print("=" * 65)

        capability = (
            NoneResultCapability(
                available=True
            )
        )

        result = capability.execute(
            "unsupported"
        )

        print(
            f"Result : {result}"
        )

        print(
            "Meaning: UNKNOWN"
        )

        self.assertIsNone(
            result
        )


    # --------------------------------------------------------
    # MODEL 2
    # --------------------------------------------------------

    def test_structured_result_success(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 2: STRUCTURED RESULT "
            "(SUCCESS)"
        )
        print("=" * 65)

        capability = (
            StructuredResultCapability(
                available=True
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Success    : "
            f"{result.success}"
        )

        print(
            f"Output     : "
            f"{result.output}"
        )

        print(
            f"Diagnostic : "
            f"{result.diagnostic}"
        )

        self.assertTrue(
            result.success
        )

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )


    def test_structured_result_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 2: STRUCTURED RESULT "
            "(CAPABILITY UNAVAILABLE)"
        )
        print("=" * 65)

        capability = (
            StructuredResultCapability(
                available=False
            )
        )

        result = capability.execute(
            "hanacaraka"
        )

        print(
            f"Success    : "
            f"{result.success}"
        )

        print(
            f"Output     : "
            f"{result.output}"
        )

        print(
            f"Diagnostic : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertIsNone(
            result.output
        )

        self.assertEqual(
            result.diagnostic,
            "Transliteration service "
            "is not available",
        )


    def test_structured_result_execution_failure(self):

        print("\n" + "=" * 65)
        print(
            "MODEL 2: STRUCTURED RESULT "
            "(EXECUTION FAILURE)"
        )
        print("=" * 65)

        capability = (
            StructuredResultCapability(
                available=True
            )
        )

        result = capability.execute(
            "unsupported"
        )

        print(
            f"Success    : "
            f"{result.success}"
        )

        print(
            f"Output     : "
            f"{result.output}"
        )

        print(
            f"Diagnostic : "
            f"{result.diagnostic}"
        )

        self.assertFalse(
            result.success
        )

        self.assertIsNone(
            result.output
        )

        self.assertEqual(
            result.diagnostic,
            "Unsupported input",
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )