import unittest


# ============================================================
# Experimental Transliteration Service
# ============================================================

class ExperimentalTransliterator:

    def transliterate(self, text):
        return f"[Service] {text}"


# ============================================================
# MODEL A
# Direct ScriptPack Method
# ============================================================

class DirectMethodScriptPack:

    def transliterate(self, text):
        return f"[Direct] {text}"


# ============================================================
# MODEL B
# ScriptPack-Owned Service
# ============================================================

class ServiceScriptPack:

    def __init__(self):
        self._transliterator = ExperimentalTransliterator()

    def get_transliterator(self):
        return self._transliterator


# ============================================================
# MODEL C
# Capability Discovery
# ============================================================

class CapabilityScriptPack:

    def __init__(self):
        self._capabilities = {
            "transliteration": ExperimentalTransliterator(),
        }

    def get_capability(self, name):
        return self._capabilities.get(name)


# ============================================================
# Experimental ScriptPack Without Transliteration
# ============================================================

class BasicScriptPack:
    """
    Test double representing a ScriptPack without
    transliteration capability.
    """

    pass


# ============================================================
# MODEL B
# ScriptPack Without Transliteration Service
# ============================================================

class ServiceOptionalScriptPack:

    def __init__(self, transliterator=None):
        self._transliterator = transliterator

    def get_transliterator(self):
        return self._transliterator


# ============================================================
# MODEL C
# ScriptPack Without Capabilities
# ============================================================

class EmptyCapabilityScriptPack:

    def __init__(self):
        self._capabilities = {}

    def get_capability(self, name):
        return self._capabilities.get(name)


# ============================================================
# Tests
# ============================================================

class TestCapabilityAccess(unittest.TestCase):

    def test_model_a_direct_method(self):
        print("\n" + "=" * 65)
        print("MODEL A: DIRECT SCRIPTPACK METHOD")
        print("=" * 65)

        scriptpack = DirectMethodScriptPack()

        result = scriptpack.transliterate("hanacaraka")

        print(f"Access : scriptpack.transliterate(text)")
        print(f"Result : {result}")

        self.assertEqual(
            result,
            "[Direct] hanacaraka"
        )

    def test_model_b_scriptpack_owned_service(self):
        print("\n" + "=" * 65)
        print("MODEL B: SCRIPTPACK-OWNED SERVICE")
        print("=" * 65)

        scriptpack = ServiceOwnedScriptPack()

        transliterator = scriptpack.get_transliterator()

        result = transliterator.transliterate("hanacaraka")

        print(
            "Access : "
            "scriptpack.get_transliterator().transliterate(text)"
        )
        print(f"Result : {result}")

        self.assertEqual(
            result,
            "[Service] hanacaraka"
        )

    def test_model_c_capability_discovery(self):
        print("\n" + "=" * 65)
        print("MODEL C: CAPABILITY DISCOVERY")
        print("=" * 65)

        scriptpack = CapabilityScriptPack()

        capability = scriptpack.get_capability("transliteration")

        result = capability.transliterate("hanacaraka")

        print(
            "Access : "
            'scriptpack.get_capability("transliteration")'
        )
        print(f"Result : {result}")

        self.assertEqual(
            result,
            "[Service] hanacaraka"
        )

    def test_model_a_missing_direct_method(self):
        print("\n" + "=" * 65)
        print("MODEL A: MISSING DIRECT METHOD")
        print("=" * 65)

        scriptpack = BasicScriptPack()

        with self.assertRaises(AttributeError):
            scriptpack.transliterate("hanacaraka")

        print("Result : AttributeError")
        print("Meaning: capability is not available")

    def test_model_b_missing_service(self):
        print("\n" + "=" * 65)
        print("MODEL B: MISSING SERVICE")
        print("=" * 65)

        scriptpack = ServiceOptionalScriptPack()

        transliterator = scriptpack.get_transliterator()

        print(
            "Access : "
            "scriptpack.get_transliterator()"
        )
        print(f"Result : {transliterator}")

        self.assertIsNone(transliterator)

    def test_model_c_missing_capability(self):
        print("\n" + "=" * 65)
        print("MODEL C: MISSING CAPABILITY")
        print("=" * 65)

        scriptpack = EmptyCapabilityScriptPack()

        capability = scriptpack.get_capability(
            "transliteration"
        )

        print(
            "Access : "
            'scriptpack.get_capability("transliteration")'
        )
        print(f"Result : {capability}")

        self.assertIsNone(capability)


if __name__ == "__main__":
    unittest.main(verbosity=2)