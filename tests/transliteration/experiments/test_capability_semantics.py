import unittest


# ============================================================
# Experimental Transliteration Result
# ============================================================

class ExperimentalResult:
    """
    Represents the result of an experimental
    transliteration execution.
    """

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
# Experimental Transliterator
# ============================================================

class ExperimentalTransliterator:
    """
    Experimental transliteration service.

    The service may successfully process input
    or return a diagnostic result.
    """

    def transliterate(self, text):

        if text == "INVALID":
            return ExperimentalResult(
                success=False,
                diagnostic="Unsupported input",
            )

        return ExperimentalResult(
            success=True,
            output=f"[Transliterated] {text}",
        )


# ============================================================
# Experimental ScriptPack
# ============================================================

class ExperimentalScriptPack:
    """
    Experimental ScriptPack used to separate:

    1. Capability support
    2. Capability availability
    3. Capability execution
    """

    def __init__(
        self,
        supports_transliteration,
        transliterator=None,
    ):
        self._supports_transliteration = (
            supports_transliteration
        )

        self._transliterator = transliterator

    def supports_transliteration(self):
        return self._supports_transliteration

    def get_transliterator(self):
        return self._transliterator


# ============================================================
# Tests
# ============================================================

class TestCapabilitySemantics(unittest.TestCase):

    # --------------------------------------------------------
    # CASE A
    # Capability Is Not Supported
    # --------------------------------------------------------

    def test_capability_not_supported(self):

        print("\n" + "=" * 65)
        print("CASE A: CAPABILITY NOT SUPPORTED")
        print("=" * 65)

        scriptpack = ExperimentalScriptPack(
            supports_transliteration=False,
        )

        supported = (
            scriptpack.supports_transliteration()
        )

        transliterator = (
            scriptpack.get_transliterator()
        )

        print(f"Supported : {supported}")
        print(f"Service   : {transliterator}")

        self.assertFalse(supported)
        self.assertIsNone(transliterator)


    # --------------------------------------------------------
    # CASE B
    # Capability Supported and Available
    # --------------------------------------------------------

    def test_capability_supported_and_available(self):

        print("\n" + "=" * 65)
        print(
            "CASE B: CAPABILITY "
            "SUPPORTED AND AVAILABLE"
        )
        print("=" * 65)

        transliterator = (
            ExperimentalTransliterator()
        )

        scriptpack = ExperimentalScriptPack(
            supports_transliteration=True,
            transliterator=transliterator,
        )

        supported = (
            scriptpack.supports_transliteration()
        )

        service = (
            scriptpack.get_transliterator()
        )

        result = service.transliterate(
            "hanacaraka"
        )

        print(f"Supported : {supported}")
        print(
            f"Service   : "
            f"{service.__class__.__name__}"
        )
        print(f"Success   : {result.success}")
        print(f"Output    : {result.output}")

        self.assertTrue(supported)
        self.assertIsNotNone(service)
        self.assertTrue(result.success)
        self.assertEqual(
            result.output,
            "[Transliterated] hanacaraka",
        )


    # --------------------------------------------------------
    # CASE C
    # Capability Supported but Unavailable
    # --------------------------------------------------------

    def test_capability_supported_but_unavailable(self):

        print("\n" + "=" * 65)
        print(
            "CASE C: CAPABILITY "
            "SUPPORTED BUT UNAVAILABLE"
        )
        print("=" * 65)

        scriptpack = ExperimentalScriptPack(
            supports_transliteration=True,
            transliterator=None,
        )

        supported = (
            scriptpack.supports_transliteration()
        )

        service = (
            scriptpack.get_transliterator()
        )

        print(f"Supported : {supported}")
        print(f"Service   : {service}")

        self.assertTrue(supported)
        self.assertIsNone(service)


    # --------------------------------------------------------
    # CASE D
    # Capability Available but Execution Fails
    # --------------------------------------------------------

    def test_capability_available_but_execution_fails(self):

        print("\n" + "=" * 65)
        print(
            "CASE D: CAPABILITY AVAILABLE "
            "BUT EXECUTION FAILS"
        )
        print("=" * 65)

        transliterator = (
            ExperimentalTransliterator()
        )

        scriptpack = ExperimentalScriptPack(
            supports_transliteration=True,
            transliterator=transliterator,
        )

        supported = (
            scriptpack.supports_transliteration()
        )

        service = (
            scriptpack.get_transliterator()
        )

        result = service.transliterate(
            "INVALID"
        )

        print(f"Supported : {supported}")
        print(
            f"Service   : "
            f"{service.__class__.__name__}"
        )
        print(f"Success   : {result.success}")
        print(
            f"Diagnostic: "
            f"{result.diagnostic}"
        )

        self.assertTrue(supported)
        self.assertIsNotNone(service)
        self.assertFalse(result.success)
        self.assertEqual(
            result.diagnostic,
            "Unsupported input",
        )


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)