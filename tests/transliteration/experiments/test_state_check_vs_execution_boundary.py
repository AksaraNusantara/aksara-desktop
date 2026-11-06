import unittest
from enum import Enum


# ============================================================
# Capability State
# ============================================================

class CapabilityState(Enum):

    AVAILABLE = "available"

    UNAVAILABLE = "unavailable"


# ============================================================
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


# ============================================================
# Experimental Service
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
# Caller-Owned State Check
# ============================================================

class CallerCheckedCapability:

    def __init__(self):

        self._state = (
            CapabilityState.AVAILABLE
        )

        self._service = (
            ExperimentalTransliterator()
        )

    def get_state(self):

        return self._state

    def set_state(
        self,
        state,
    ):

        self._state = state

    def execute(
        self,
        text,
    ):

        # Model A deliberately trusts caller.
        return (
            self._service
            .transliterate(text)
        )


# ============================================================
# MODEL B
#
# Capability-Owned Execution Guard
# ============================================================

class GuardedCapability:

    def __init__(self):

        self._state = (
            CapabilityState.AVAILABLE
        )

        self._service = (
            ExperimentalTransliterator()
        )

    def get_state(self):

        return self._state

    def set_state(
        self,
        state,
    ):

        self._state = state

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
                    "Capability is not "
                    "available"
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
# MODEL C
#
# Hybrid Boundary
# ============================================================

class HybridCapability:

    def __init__(self):

        self._state = (
            CapabilityState.AVAILABLE
        )

        self._service = (
            ExperimentalTransliterator()
        )

    def get_state(self):

        return self._state

    def set_state(
        self,
        state,
    ):

        self._state = state

    def execute(
        self,
        text,
    ):

        # Internal guard remains authoritative.
        if (
            self._state
            != CapabilityState.AVAILABLE
        ):

            return BoundaryResponse(
                executed=False,
                reason=(
                    "Capability state "
                    "does not permit execution"
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
# Tests
# ============================================================

class TestStateCheckVsExecutionBoundary(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    #
    # Caller checks state.
    # State changes before execution.
    # --------------------------------------------------------

    def test_model_a_state_changes_after_check(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL A: CALLER-OWNED STATE CHECK"
        )
        print("=" * 65)

        capability = (
            CallerCheckedCapability()
        )

        state = (
            capability.get_state()
        )

        print(
            f"State Check : "
            f"{state.name}"
        )

        self.assertEqual(
            state,
            CapabilityState.AVAILABLE,
        )

        # State changes after caller check.
        capability.set_state(
            CapabilityState.UNAVAILABLE
        )

        print(
            "State Change: "
            "UNAVAILABLE"
        )

        output = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            "Execution   : "
            "STILL EXECUTED"
        )

        print(
            f"Output      : {output}"
        )

        self.assertEqual(
            output,
            "[Transliterated] hanacaraka",
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Capability protects its own boundary.
    # --------------------------------------------------------

    def test_model_b_internal_guard_blocks_execution(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL B: CAPABILITY-OWNED GUARD"
        )
        print("=" * 65)

        capability = (
            GuardedCapability()
        )

        capability.set_state(
            CapabilityState.UNAVAILABLE
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"State       : "
            f"{capability.get_state().name}"
        )

        print(
            f"Executed    : "
            f"{result.executed}"
        )

        print(
            f"Reason      : "
            f"{result.reason}"
        )

        self.assertFalse(
            result.executed
        )

        self.assertIsNone(
            result.output
        )


    # --------------------------------------------------------
    # MODEL B
    #
    # Execution proceeds when state allows it.
    # --------------------------------------------------------

    def test_model_b_internal_guard_allows_execution(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL B: GUARD ALLOWS EXECUTION"
        )
        print("=" * 65)

        capability = (
            GuardedCapability()
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"State       : "
            f"{capability.get_state().name}"
        )

        print(
            f"Executed    : "
            f"{result.executed}"
        )

        print(
            f"Output      : "
            f"{result.output}"
        )

        self.assertTrue(
            result.executed
        )

        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )


    # --------------------------------------------------------
    # MODEL C
    #
    # Caller receives state information.
    # Capability remains protected.
    # --------------------------------------------------------

    def test_model_c_caller_can_inspect_state(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL C: HYBRID BOUNDARY"
        )
        print("=" * 65)

        capability = (
            HybridCapability()
        )

        state = (
            capability.get_state()
        )

        print(
            f"Reported State : "
            f"{state.name}"
        )

        self.assertEqual(
            state,
            CapabilityState.AVAILABLE,
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Executed       : "
            f"{result.executed}"
        )

        print(
            f"Output         : "
            f"{result.output}"
        )

        self.assertTrue(
            result.executed
        )


    # --------------------------------------------------------
    # MODEL C
    #
    # State changes after caller inspection.
    # Internal guard remains authoritative.
    # --------------------------------------------------------

    def test_model_c_guard_handles_state_change(
        self,
    ):

        print("\n" + "=" * 65)
        print(
            "MODEL C: STATE CHANGE AFTER CHECK"
        )
        print("=" * 65)

        capability = (
            HybridCapability()
        )

        state = (
            capability.get_state()
        )

        print(
            f"Initial State : "
            f"{state.name}"
        )

        self.assertEqual(
            state,
            CapabilityState.AVAILABLE,
        )

        # Simulate a state change after inspection.
        capability.set_state(
            CapabilityState.UNAVAILABLE
        )

        print(
            "State Change  : "
            "UNAVAILABLE"
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Executed      : "
            f"{result.executed}"
        )

        print(
            f"Reason        : "
            f"{result.reason}"
        )

        self.assertFalse(
            result.executed
        )

        self.assertIsNone(
            result.output
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )