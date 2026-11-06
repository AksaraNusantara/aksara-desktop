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
# Capability Status
# ============================================================

class CapabilityStatus:
    """
    Experimental representation of a capability state.

    This object separates the state of a capability
    from optional diagnostic information.
    """

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
# Experimental ScriptPack
# ============================================================

class ExperimentalScriptPack:

    def __init__(
        self,
        capability_status,
    ):
        self._capability_status = (
            capability_status
        )

    def get_transliteration_status(self):
        return self._capability_status


# ============================================================
# Application Caller
# ============================================================

class ApplicationCaller:
    """
    Represents a caller that only needs to know
    whether transliteration can currently be used.
    """

    def can_use_transliteration(
        self,
        scriptpack,
    ):
        status = (
            scriptpack.get_transliteration_status()
        )

        return status.is_available()


# ============================================================
# Feature Controller
# ============================================================

class FeatureController:
    """
    Represents a caller that needs to determine
    why a feature cannot be used.
    """

    def get_feature_state(
        self,
        scriptpack,
    ):
        status = (
            scriptpack.get_transliteration_status()
        )

        return status.state


# ============================================================
# Diagnostic Tool
# ============================================================

class DiagnosticTool:
    """
    Represents a caller that requires complete
    capability information.
    """

    def inspect_transliteration(
        self,
        scriptpack,
    ):
        status = (
            scriptpack.get_transliteration_status()
        )

        return {
            "state": status.state,
            "reason": status.reason,
        }


# ============================================================
# Tests
# ============================================================

class TestCapabilityCallerPerspective(
    unittest.TestCase
):

    # --------------------------------------------------------
    # Application Caller
    # --------------------------------------------------------

    def test_application_caller(self):

        print("\n" + "=" * 65)
        print("APPLICATION CALLER")
        print("=" * 65)

        caller = ApplicationCaller()

        scenarios = {

            "Unsupported": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.UNSUPPORTED,
                    reason=(
                        "Transliteration is not "
                        "provided by this ScriptPack"
                    ),
                )
            ),

            "Available": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.AVAILABLE,
                )
            ),

            "Unavailable": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.UNAVAILABLE,
                    reason=(
                        "Transliteration service "
                        "is not initialized"
                    ),
                )
            ),
        }

        results = {}

        for name, scriptpack in scenarios.items():

            usable = (
                caller.can_use_transliteration(
                    scriptpack
                )
            )

            results[name] = usable

            print(
                f"{name:<12}: "
                f"Can use = {usable}"
            )

        self.assertFalse(
            results["Unsupported"]
        )

        self.assertTrue(
            results["Available"]
        )

        self.assertFalse(
            results["Unavailable"]
        )


    # --------------------------------------------------------
    # Feature Controller
    # --------------------------------------------------------

    def test_feature_controller(self):

        print("\n" + "=" * 65)
        print("FEATURE CONTROLLER")
        print("=" * 65)

        controller = FeatureController()

        scenarios = {

            "Unsupported": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.UNSUPPORTED
                )
            ),

            "Available": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.AVAILABLE
                )
            ),

            "Unavailable": ExperimentalScriptPack(
                CapabilityStatus(
                    CapabilityState.UNAVAILABLE
                )
            ),
        }

        results = {}

        for name, scriptpack in scenarios.items():

            state = (
                controller.get_feature_state(
                    scriptpack
                )
            )

            results[name] = state

            print(
                f"{name:<12}: "
                f"State = {state.name}"
            )

        self.assertEqual(
            results["Unsupported"],
            CapabilityState.UNSUPPORTED,
        )

        self.assertEqual(
            results["Available"],
            CapabilityState.AVAILABLE,
        )

        self.assertEqual(
            results["Unavailable"],
            CapabilityState.UNAVAILABLE,
        )


    # --------------------------------------------------------
    # Diagnostic Tool
    # --------------------------------------------------------

    def test_diagnostic_tool(self):

        print("\n" + "=" * 65)
        print("DIAGNOSTIC / DEVELOPER TOOL")
        print("=" * 65)

        diagnostic = DiagnosticTool()

        scriptpack = ExperimentalScriptPack(
            CapabilityStatus(
                CapabilityState.UNAVAILABLE,
                reason=(
                    "Transliteration service "
                    "is not initialized"
                ),
            )
        )

        result = (
            diagnostic.inspect_transliteration(
                scriptpack
            )
        )

        print(
            f"State  : "
            f"{result['state'].name}"
        )

        print(
            f"Reason : "
            f"{result['reason']}"
        )

        self.assertEqual(
            result["state"],
            CapabilityState.UNAVAILABLE,
        )

        self.assertEqual(
            result["reason"],
            "Transliteration service "
            "is not initialized",
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)