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
# MODEL A
# Immediately Available
# ============================================================

class ImmediatelyAvailableCapability:

    def get_status(self):

        return CapabilityStatus(
            CapabilityState.AVAILABLE
        )


# ============================================================
# MODEL B
# Explicit Initialization
# ============================================================

class ExplicitInitializationCapability:

    def __init__(self):

        self._initialized = False

    def initialize(self):

        self._initialized = True

    def get_status(self):

        if self._initialized:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Capability has not been "
                "initialized"
            ),
        )


# ============================================================
# MODEL C
# Initialization Failure
# ============================================================

class FailingInitializationCapability:

    def __init__(self):

        self._initialized = False

        self._failure_reason = None

    def initialize(self):

        self._initialized = False

        self._failure_reason = (
            "Required transliteration "
            "resource could not be loaded"
        )

    def get_status(self):

        if self._initialized:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        if self._failure_reason:

            return CapabilityStatus(
                CapabilityState.UNAVAILABLE,
                reason=self._failure_reason,
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Capability has not been "
                "initialized"
            ),
        )


# ============================================================
# Tests
# ============================================================

class TestCapabilityLifecycle(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    # --------------------------------------------------------

    def test_immediately_available(self):

        print("\n" + "=" * 65)
        print("MODEL A: IMMEDIATELY AVAILABLE")
        print("=" * 65)

        capability = (
            ImmediatelyAvailableCapability()
        )

        status = (
            capability.get_status()
        )

        print(
            f"State  : "
            f"{status.state.name}"
        )

        print(
            f"Reason : "
            f"{status.reason}"
        )

        self.assertEqual(
            status.state,
            CapabilityState.AVAILABLE,
        )

        self.assertTrue(
            status.is_available()
        )


    # --------------------------------------------------------
    # MODEL B
    # --------------------------------------------------------

    def test_explicit_initialization(self):

        print("\n" + "=" * 65)
        print("MODEL B: EXPLICIT INITIALIZATION")
        print("=" * 65)

        capability = (
            ExplicitInitializationCapability()
        )

        print("\nBefore initialization:")

        before_status = (
            capability.get_status()
        )

        print(
            f"State  : "
            f"{before_status.state.name}"
        )

        print(
            f"Reason : "
            f"{before_status.reason}"
        )

        capability.initialize()

        print("\nAfter initialization:")

        after_status = (
            capability.get_status()
        )

        print(
            f"State  : "
            f"{after_status.state.name}"
        )

        print(
            f"Reason : "
            f"{after_status.reason}"
        )

        self.assertEqual(
            before_status.state,
            CapabilityState.UNAVAILABLE,
        )

        self.assertEqual(
            after_status.state,
            CapabilityState.AVAILABLE,
        )

        self.assertFalse(
            before_status.is_available()
        )

        self.assertTrue(
            after_status.is_available()
        )


    # --------------------------------------------------------
    # MODEL C
    # --------------------------------------------------------

    def test_initialization_failure(self):

        print("\n" + "=" * 65)
        print("MODEL C: INITIALIZATION FAILURE")
        print("=" * 65)

        capability = (
            FailingInitializationCapability()
        )

        print("\nBefore initialization:")

        before_status = (
            capability.get_status()
        )

        print(
            f"State  : "
            f"{before_status.state.name}"
        )

        print(
            f"Reason : "
            f"{before_status.reason}"
        )

        capability.initialize()

        print("\nAfter initialization attempt:")

        after_status = (
            capability.get_status()
        )

        print(
            f"State  : "
            f"{after_status.state.name}"
        )

        print(
            f"Reason : "
            f"{after_status.reason}"
        )

        self.assertEqual(
            before_status.state,
            CapabilityState.UNAVAILABLE,
        )

        self.assertEqual(
            after_status.state,
            CapabilityState.UNAVAILABLE,
        )

        self.assertNotEqual(
            before_status.reason,
            after_status.reason,
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)