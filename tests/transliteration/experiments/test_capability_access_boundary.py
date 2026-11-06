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
# Transliterator Service
# ============================================================

class ExperimentalTransliterator:

    def transliterate(
        self,
        text,
    ):

        return (
            f"[Transliterated] {text}"
        )


# ============================================================
# MODEL A
# Separate Status and Service Access
# ============================================================

class SeparateAccessScriptPack:

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

    def get_capability_status(
        self,
        capability_name,
    ):

        if capability_name != "transliteration":

            return CapabilityStatus(
                CapabilityState.UNAVAILABLE,
                reason=(
                    "Capability is not supported"
                ),
            )

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

    def get_transliterator(self):

        return self._service


# ============================================================
# MODEL B
# Unified Capability Object
# ============================================================

class TransliterationCapability:

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

    def is_available(self):

        return (
            self.get_status()
            .is_available()
        )

    def execute(
        self,
        text,
    ):

        if not self.is_available():

            return None

        return (
            self._service
            .transliterate(text)
        )


class UnifiedCapabilityScriptPack:

    def __init__(
        self,
        available=True,
    ):

        self._capability = (
            TransliterationCapability(
                available=available
            )
        )

    def get_capability(
        self,
        capability_name,
    ):

        if capability_name != "transliteration":

            return None

        return self._capability


# ============================================================
# Tests
# ============================================================

class TestCapabilityAccessBoundary(
    unittest.TestCase
):

    # --------------------------------------------------------
    # MODEL A
    # --------------------------------------------------------

    def test_model_a_separate_access_available(self):

        print("\n" + "=" * 65)
        print(
            "MODEL A: SEPARATE ACCESS "
            "(AVAILABLE)"
        )
        print("=" * 65)

        scriptpack = (
            SeparateAccessScriptPack(
                available=True
            )
        )

        status = (
            scriptpack
            .get_capability_status(
                "transliteration"
            )
        )

        print(
            f"Status : "
            f"{status.state.name}"
        )

        self.assertTrue(
            status.is_available()
        )

        service = (
            scriptpack
            .get_transliterator()
        )

        print(
            f"Service: "
            f"{service.__class__.__name__}"
        )

        result = (
            service
            .transliterate(
                "hanacaraka"
            )
        )

        print(
            f"Result : {result}"
        )

        self.assertEqual(
            result,
            "[Transliterated] hanacaraka",
        )


    def test_model_a_separate_access_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "MODEL A: SEPARATE ACCESS "
            "(UNAVAILABLE)"
        )
        print("=" * 65)

        scriptpack = (
            SeparateAccessScriptPack(
                available=False
            )
        )

        status = (
            scriptpack
            .get_capability_status(
                "transliteration"
            )
        )

        print(
            f"Status : "
            f"{status.state.name}"
        )

        print(
            f"Reason : "
            f"{status.reason}"
        )

        self.assertFalse(
            status.is_available()
        )

        service = (
            scriptpack
            .get_transliterator()
        )

        print(
            f"Service: {service}"
        )

        self.assertIsNone(
            service
        )


    # --------------------------------------------------------
    # MODEL B
    # --------------------------------------------------------

    def test_model_b_unified_capability_available(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: UNIFIED CAPABILITY "
            "(AVAILABLE)"
        )
        print("=" * 65)

        scriptpack = (
            UnifiedCapabilityScriptPack(
                available=True
            )
        )

        capability = (
            scriptpack
            .get_capability(
                "transliteration"
            )
        )

        status = (
            capability.get_status()
        )

        print(
            f"Status : "
            f"{status.state.name}"
        )

        self.assertTrue(
            capability.is_available()
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Result : {result}"
        )

        self.assertEqual(
            result,
            "[Transliterated] hanacaraka",
        )


    def test_model_b_unified_capability_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "MODEL B: UNIFIED CAPABILITY "
            "(UNAVAILABLE)"
        )
        print("=" * 65)

        scriptpack = (
            UnifiedCapabilityScriptPack(
                available=False
            )
        )

        capability = (
            scriptpack
            .get_capability(
                "transliteration"
            )
        )

        status = (
            capability.get_status()
        )

        print(
            f"Status : "
            f"{status.state.name}"
        )

        print(
            f"Reason : "
            f"{status.reason}"
        )

        self.assertFalse(
            capability.is_available()
        )

        result = (
            capability.execute(
                "hanacaraka"
            )
        )

        print(
            f"Result : {result}"
        )

        self.assertIsNone(
            result
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )