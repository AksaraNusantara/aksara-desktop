import unittest
from enum import Enum


# ============================================================
# Shared Capability State
# ============================================================

class CapabilityState(Enum):

    UNSUPPORTED = "unsupported"

    AVAILABLE = "available"

    UNAVAILABLE = "unavailable"


class CapabilityStatus:

    def __init__(
        self,
        state,
        reason=None,
    ):
        self.state = state
        self.reason = reason


# ============================================================
# MODEL A
# ScriptPack-Owned Status
# ============================================================

class ScriptPackOwnedStatus:

    def __init__(
        self,
        transliteration_available,
    ):
        self._transliteration_available = (
            transliteration_available
        )

    def get_transliteration_status(self):

        if self._transliteration_available:

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


# ============================================================
# MODEL B
# Engine-Owned Status
# ============================================================

class CapabilityScriptPack:

    def supports_transliteration(self):
        return True


class TransliterationEngine:

    def __init__(
        self,
        transliteration_available,
    ):
        self._transliteration_available = (
            transliteration_available
        )

    def get_transliteration_status(
        self,
        scriptpack,
    ):

        if not scriptpack.supports_transliteration():

            return CapabilityStatus(
                CapabilityState.UNSUPPORTED
            )

        if self._transliteration_available:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Runtime engine could not "
                "initialize transliteration"
            ),
        )


# ============================================================
# MODEL C
# Runtime-Resolved Status
# ============================================================

class DeclaredCapabilityScriptPack:

    def declares_transliteration(self):
        return True


class CapabilityRuntimeResolver:

    def __init__(
        self,
        resource_available,
    ):
        self._resource_available = (
            resource_available
        )

    def resolve_transliteration(
        self,
        scriptpack,
    ):

        if not scriptpack.declares_transliteration():

            return CapabilityStatus(
                CapabilityState.UNSUPPORTED
            )

        if self._resource_available:

            return CapabilityStatus(
                CapabilityState.AVAILABLE
            )

        return CapabilityStatus(
            CapabilityState.UNAVAILABLE,
            reason=(
                "Required runtime resource "
                "was not found"
            ),
        )


# ============================================================
# Tests
# ============================================================

class TestCapabilityOwnership(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    # --------------------------------------------------------

    def test_model_a_scriptpack_owned_status(self):

        print("\n" + "=" * 65)
        print("MODEL A: SCRIPTPACK-OWNED STATUS")
        print("=" * 65)

        available_scriptpack = (
            ScriptPackOwnedStatus(
                transliteration_available=True
            )
        )

        unavailable_scriptpack = (
            ScriptPackOwnedStatus(
                transliteration_available=False
            )
        )

        available_status = (
            available_scriptpack
            .get_transliteration_status()
        )

        unavailable_status = (
            unavailable_scriptpack
            .get_transliteration_status()
        )

        print("\nAvailable ScriptPack:")
        print(
            f"State  : "
            f"{available_status.state.name}"
        )

        print("\nUnavailable ScriptPack:")
        print(
            f"State  : "
            f"{unavailable_status.state.name}"
        )
        print(
            f"Reason : "
            f"{unavailable_status.reason}"
        )

        self.assertEqual(
            available_status.state,
            CapabilityState.AVAILABLE,
        )

        self.assertEqual(
            unavailable_status.state,
            CapabilityState.UNAVAILABLE,
        )


    # --------------------------------------------------------
    # MODEL B
    # --------------------------------------------------------

    def test_model_b_engine_owned_status(self):

        print("\n" + "=" * 65)
        print("MODEL B: ENGINE-OWNED STATUS")
        print("=" * 65)

        scriptpack = CapabilityScriptPack()

        available_engine = (
            TransliterationEngine(
                transliteration_available=True
            )
        )

        unavailable_engine = (
            TransliterationEngine(
                transliteration_available=False
            )
        )

        available_status = (
            available_engine
            .get_transliteration_status(
                scriptpack
            )
        )

        unavailable_status = (
            unavailable_engine
            .get_transliteration_status(
                scriptpack
            )
        )

        print("\nAvailable Engine:")
        print(
            f"State  : "
            f"{available_status.state.name}"
        )

        print("\nUnavailable Engine:")
        print(
            f"State  : "
            f"{unavailable_status.state.name}"
        )
        print(
            f"Reason : "
            f"{unavailable_status.reason}"
        )

        self.assertEqual(
            available_status.state,
            CapabilityState.AVAILABLE,
        )

        self.assertEqual(
            unavailable_status.state,
            CapabilityState.UNAVAILABLE,
        )


    # --------------------------------------------------------
    # MODEL C
    # --------------------------------------------------------

    def test_model_c_runtime_resolved_status(self):

        print("\n" + "=" * 65)
        print("MODEL C: RUNTIME-RESOLVED STATUS")
        print("=" * 65)

        scriptpack = (
            DeclaredCapabilityScriptPack()
        )

        available_runtime = (
            CapabilityRuntimeResolver(
                resource_available=True
            )
        )

        unavailable_runtime = (
            CapabilityRuntimeResolver(
                resource_available=False
            )
        )

        available_status = (
            available_runtime
            .resolve_transliteration(
                scriptpack
            )
        )

        unavailable_status = (
            unavailable_runtime
            .resolve_transliteration(
                scriptpack
            )
        )

        print("\nAvailable Runtime:")
        print(
            f"State  : "
            f"{available_status.state.name}"
        )

        print("\nUnavailable Runtime:")
        print(
            f"State  : "
            f"{unavailable_status.state.name}"
        )
        print(
            f"Reason : "
            f"{unavailable_status.reason}"
        )

        self.assertEqual(
            available_status.state,
            CapabilityState.AVAILABLE,
        )

        self.assertEqual(
            unavailable_status.state,
            CapabilityState.UNAVAILABLE,
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)