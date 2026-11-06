import unittest
from enum import Enum


# ============================================================
# MODEL 1
# Boolean State Representation
# ============================================================

class BooleanCapabilityState:
    """
    Represent capability state using separate boolean values.
    """

    def __init__(
        self,
        supported,
        available,
    ):
        self.supported = supported
        self.available = available


# ============================================================
# MODEL 2
# Enum State Representation
# ============================================================

class CapabilityState(Enum):

    UNSUPPORTED = "unsupported"

    AVAILABLE = "available"

    UNAVAILABLE = "unavailable"


# ============================================================
# MODEL 3
# Capability Descriptor
# ============================================================

class CapabilityDescriptor:
    """
    Represent capability state together with
    optional diagnostic information.
    """

    def __init__(
        self,
        supported,
        available,
        reason=None,
    ):
        self.supported = supported
        self.available = available
        self.reason = reason


# ============================================================
# Tests
# ============================================================

class TestCapabilityStateRepresentation(unittest.TestCase):

    # --------------------------------------------------------
    # MODEL 1
    # Boolean Representation
    # --------------------------------------------------------

    def test_boolean_state_representation(self):

        print("\n" + "=" * 65)
        print("MODEL 1: BOOLEAN STATE REPRESENTATION")
        print("=" * 65)

        states = {
            "Unsupported": BooleanCapabilityState(
                supported=False,
                available=False,
            ),
            "Available": BooleanCapabilityState(
                supported=True,
                available=True,
            ),
            "Unavailable": BooleanCapabilityState(
                supported=True,
                available=False,
            ),
        }

        for name, state in states.items():

            print(f"\nState     : {name}")
            print(f"Supported : {state.supported}")
            print(f"Available : {state.available}")

        self.assertFalse(
            states["Unsupported"].supported
        )

        self.assertTrue(
            states["Available"].supported
        )

        self.assertTrue(
            states["Available"].available
        )

        self.assertTrue(
            states["Unavailable"].supported
        )

        self.assertFalse(
            states["Unavailable"].available
        )


    # --------------------------------------------------------
    # MODEL 2
    # Enum Representation
    # --------------------------------------------------------

    def test_enum_state_representation(self):

        print("\n" + "=" * 65)
        print("MODEL 2: ENUM STATE REPRESENTATION")
        print("=" * 65)

        states = [
            CapabilityState.UNSUPPORTED,
            CapabilityState.AVAILABLE,
            CapabilityState.UNAVAILABLE,
        ]

        for state in states:

            print(
                f"State : {state.name}"
            )

        self.assertEqual(
            CapabilityState.UNSUPPORTED.value,
            "unsupported",
        )

        self.assertEqual(
            CapabilityState.AVAILABLE.value,
            "available",
        )

        self.assertEqual(
            CapabilityState.UNAVAILABLE.value,
            "unavailable",
        )


    # --------------------------------------------------------
    # MODEL 3
    # Capability Descriptor
    # --------------------------------------------------------

    def test_capability_descriptor(self):

        print("\n" + "=" * 65)
        print("MODEL 3: CAPABILITY DESCRIPTOR")
        print("=" * 65)

        states = {
            "Unsupported": CapabilityDescriptor(
                supported=False,
                available=False,
                reason=(
                    "Capability is not provided "
                    "by this ScriptPack"
                ),
            ),

            "Available": CapabilityDescriptor(
                supported=True,
                available=True,
            ),

            "Unavailable": CapabilityDescriptor(
                supported=True,
                available=False,
                reason=(
                    "Transliteration service "
                    "is not initialized"
                ),
            ),
        }

        for name, state in states.items():

            print(f"\nState     : {name}")
            print(f"Supported : {state.supported}")
            print(f"Available : {state.available}")

            if state.reason is not None:

                print(
                    f"Reason    : {state.reason}"
                )

        self.assertFalse(
            states["Unsupported"].supported
        )

        self.assertTrue(
            states["Available"].available
        )

        self.assertFalse(
            states["Unavailable"].available
        )

        self.assertIsNotNone(
            states["Unavailable"].reason
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)