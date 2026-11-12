"""
===============================================================================

Aksara Nusantara

Module:
    tests.test_transliteration_javanese

Module Type:
    Unit / Integration Test

Purpose:
    Verifies the Javanese ScriptPack transliteration engine against the
    LOCKED AD-TR-01 contract rules and golden cases, through the Core
    Transliteration API (TD-001).

References:
    docs/development/transliteration/06. AD-TR-01 — Transliteration Contract Rules v0_1.md

    tests/transliteration/contract_review/test_ng_cases.py

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

import subprocess
import sys
import unittest
from pathlib import Path

# =============================================================================
# Local Project Imports
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.engine import CoreEngine
from core.exceptions import TransliterationError
from core.transliteration import DiagnosticCode
from core.transliteration import TransliterationDirection
from core.transliteration import TransliterationResult


LATIN = TransliterationDirection.LATIN_TO_SCRIPT
SCRIPT = TransliterationDirection.SCRIPT_TO_LATIN

PANGKON = "꧀"
TALING = "ꦺ"
TARUNG = "ꦴ"
CAKRA = "ꦿ"


def _build_engine() -> CoreEngine:
    engine = CoreEngine()
    engine.initialize(PROJECT_ROOT / "scriptpacks")
    engine.activate("javanese")
    return engine


class _JavaneseCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = _build_engine()

    def forward(self, text: str) -> TransliterationResult:
        return self.engine.transliterate(text, LATIN)

    def reverse(self, text: str) -> TransliterationResult:
        return self.engine.transliterate(text, SCRIPT)

    def codes(self, result: TransliterationResult) -> list[DiagnosticCode]:
        return [diagnostic.code for diagnostic in result.diagnostics]


class TestGoldenCases(_JavaneseCase):
    """AD-TR-01 §24 — Golden Test Seed."""

    FORWARD = {
        "ka": "ꦏ",
        "ki": "ꦏꦶ",
        "ku": "ꦏꦸ",
        "keu": "ꦏꦼ",
        "ke": "ꦏꦺ",
        "ko": "ꦏꦺꦴ",
        "k": "ꦏ꧀",
        "kah": "ꦏꦃ",
        "kar": "ꦏꦂ",
        "kang": "ꦏꦁ",
        "kra": "ꦏꦿ",
        "kya": "ꦏꦾ",
        "kreu": "ꦏꦽ",
        "kh": "ꦏ꦳",
        "gh": "ꦒ꦳",
        "dz": "ꦢ꦳",
        "f": "ꦥ꦳",
        "v": "ꦮ꦳",
        "z": "ꦗ꦳",
        "a": "ꦄ",
        "i": "ꦆ",
        "u": "ꦈ",
        "e": "ꦌ",
        "o": "ꦎ",
        "123": "꧑꧒꧓",
        ",": "꧈",
        ".": "꧉",
    }

    REVERSE = {
        "ꦏ": "ka",
        "ꦏꦶ": "ki",
        "ꦏ꧀": "k",
        "ꦏꦃ": "kah",
        "ꦏꦂ": "kar",
        "ꦏꦁ": "kang",
        "ꦏꦿ": "kra",
        "ꦏꦾ": "kya",
        "ꦏ꦳": "kh",
        "ꦑ": "k",
        "꧑꧒꧓": "123",
    }

    def test_forward_golden_cases(self):
        for latin, expected in self.FORWARD.items():
            with self.subTest(latin=latin):
                result = self.forward(latin)
                self.assertEqual(result.output, expected)
                self.assertEqual(result.diagnostics, ())

    def test_reverse_golden_cases(self):
        for javanese, expected in self.REVERSE.items():
            with self.subTest(javanese=javanese):
                result = self.reverse(javanese)
                self.assertEqual(result.output, expected)
                self.assertEqual(result.diagnostics, ())


class TestAbugidaRules(_JavaneseCase):

    def test_words(self):
        cases = {
            "hanacaraka": "ꦲꦤꦕꦫꦏ",
            "aksara": "ꦄꦏ꧀ꦱꦫ",
            "pitik": "ꦥꦶꦠꦶꦏ꧀",
            "sastra": "ꦱꦱ꧀ꦠꦿ",
            "karya": "ꦏꦂꦪ",
        }

        for latin, expected in cases.items():
            with self.subTest(latin=latin):
                self.assertEqual(self.forward(latin).output, expected)
                self.assertEqual(self.reverse(expected).output, latin)

    def test_taling_is_stored_after_host_in_logical_order(self):
        self.assertEqual(self.forward("ke").output, "ꦏ" + TALING)
        self.assertEqual(self.forward("kre").output, "ꦏ" + CAKRA + TALING)
        self.assertEqual(
            self.forward("kte").output,
            "ꦏ" + PANGKON + "ꦠ" + TALING,
        )

    def test_taling_tarung_wraps_the_host(self):
        self.assertEqual(self.forward("ko").output, "ꦏ" + TALING + TARUNG)
        self.assertEqual(self.reverse("ꦏꦺꦴꦤ꧀").output, "kon")

    def test_visual_order_taling_is_invalid_context(self):
        result = self.reverse(TALING + "ꦏ")

        self.assertEqual(result.output, TALING + "ka")
        self.assertEqual(self.codes(result), [DiagnosticCode.INVALID_CONTEXT])
        self.assertIn("logical order", result.diagnostics[0].message)

    def test_pasangan_is_a_consonant_sequence(self):
        self.assertEqual(self.forward("kma").output, "ꦏ꧀ꦩ")
        self.assertEqual(self.reverse("ꦏ꧀ꦩ").output, "kma")

    def test_pangkon_removes_inherent_vowel(self):
        self.assertEqual(self.forward("kak").output, "ꦏꦏ꧀")
        self.assertEqual(self.reverse("ꦏꦏ꧀").output, "kak")

    def test_panyigeg_closes_syllable_before_consonant(self):
        self.assertEqual(self.forward("karta").output, "ꦏꦂꦠ")
        self.assertEqual(self.forward("kahna").output, "ꦏꦃꦤ")

    def test_rekan_token_is_not_split(self):
        self.assertEqual(self.forward("khi").output, "ꦏ꦳ꦶ")
        self.assertEqual(self.reverse("ꦏ꦳ꦶ").output, "khi")

    def test_murda_follows_current_scriptpack_data(self):
        self.assertEqual(self.forward("ka").output, "ꦏ")
        self.assertEqual(self.reverse("ꦑꦶ").output, "ki")

    def test_uppercase_latin_is_matched_case_insensitively(self):
        self.assertEqual(self.forward("Ka").output, "ꦏ")


class TestNgContractReview(_JavaneseCase):
    """TR-CR-001 — only single-candidate cases are resolved."""

    def test_resolved_cases(self):
        self.assertEqual(self.forward("nga").output, "ꦔ")
        self.assertEqual(self.forward("kang").output, "ꦏꦁ")

    def test_open_cases_are_preserved_with_diagnostic(self):
        cases = {
            "ng": "ng",
            "ngka": "ngꦏ",
            "angka": "ꦄngꦏ",
        }

        for latin, expected in cases.items():
            with self.subTest(latin=latin):
                result = self.forward(latin)

                self.assertEqual(result.output, expected)
                self.assertEqual(
                    self.codes(result), [DiagnosticCode.OPEN_CONTRACT],
                )
                self.assertEqual(result.diagnostics[0].segment, "ng")
                self.assertEqual(result.diagnostics[0].rule, "TR-CR-001")
                self.assertFalse(result.is_complete)


class TestDiagnostics(_JavaneseCase):
    """AD-TR-01 §22 and §23."""

    def test_unsupported_sequence(self):
        result = self.forward("kry")

        self.assertEqual(result.output, "kry")
        self.assertEqual(
            self.codes(result), [DiagnosticCode.UNSUPPORTED_SEQUENCE],
        )
        self.assertEqual(
            (result.diagnostics[0].start, result.diagnostics[0].end), (0, 3),
        )

    def test_sandhangan_without_host(self):
        result = self.reverse("ꦶ")

        self.assertEqual(result.output, "ꦶ")
        self.assertEqual(self.codes(result), [DiagnosticCode.INVALID_CONTEXT])

    def test_partial_processing_keeps_valid_segments(self):
        result = self.forward("kry ka")

        self.assertEqual(result.output, "kry ꦏ")
        self.assertEqual(len(result.diagnostics), 1)

    def test_unknown_characters_are_preserved(self):
        result = self.forward("ka@#")

        self.assertEqual(result.output, "ꦏ@#")
        self.assertEqual(
            self.codes(result),
            [DiagnosticCode.UNKNOWN, DiagnosticCode.UNKNOWN],
        )
        self.assertTrue(result.is_complete)

    def test_unmapped_punctuation_is_preserved(self):
        self.assertEqual(self.forward("ka?!:;").output, "ꦏ?!:;")

    def test_open_pada_is_reported(self):
        result = self.reverse("꧇")

        self.assertEqual(result.output, "꧇")
        self.assertEqual(self.codes(result), [DiagnosticCode.OPEN_CONTRACT])


class TestCrossCuttingRules(_JavaneseCase):

    def test_whitespace_is_preserved(self):
        text = "  ka\tki\nku  "

        self.assertEqual(self.forward(text).output, "  ꦏ\tꦏꦶ\nꦏꦸ  ")
        self.assertEqual(
            self.reverse("  ꦏ\tꦏꦶ\nꦏꦸ  ").output, text,
        )

    def test_determinism(self):
        text = "aksara jawa, sastra."

        self.assertEqual(self.forward(text), self.forward(text))

    def test_engine_module_has_no_ui_dependency(self):
        module_path = (
            PROJECT_ROOT / "scriptpacks" / "javanese" / "transliteration.py"
        )

        code = (
            "import importlib.util, sys\n"
            f"sys.path.insert(0, {str(PROJECT_ROOT)!r})\n"
            f"spec = importlib.util.spec_from_file_location('m', {str(module_path)!r})\n"
            "module = importlib.util.module_from_spec(spec)\n"
            "sys.modules['m'] = module\n"
            "spec.loader.exec_module(module)\n"
            "assert not any(name.startswith('PySide6') for name in sys.modules)\n"
        )

        completed = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)


class TestCoreTransliterationApi(unittest.TestCase):
    """AD-TR-01 TD-001 — the Core Engine dispatches, it does not transliterate."""

    @classmethod
    def setUpClass(cls):
        cls.engine = CoreEngine()
        cls.engine.initialize(PROJECT_ROOT / "scriptpacks")

    def test_requires_a_scriptpack(self):
        engine = CoreEngine()

        with self.assertRaises(TransliterationError):
            engine.transliterate("ka", LATIN)

    def test_explicit_identifier(self):
        result = self.engine.transliterate("ka", LATIN, "javanese")

        self.assertIsInstance(result, TransliterationResult)
        self.assertEqual(result.output, "ꦏ")
        self.assertIs(result.direction, LATIN)

    def test_direction_value_is_accepted(self):
        result = self.engine.transliterate("ꦏ", "script_to_latin", "javanese")

        self.assertEqual(result.output, "ka")

    def test_scriptpack_without_support_is_rejected(self):
        with self.assertRaises(TransliterationError):
            self.engine.transliterate("ka", LATIN, "sample")

    def test_text_must_be_str(self):
        with self.assertRaises(TypeError):
            self.engine.transliterate(None, LATIN, "javanese")


if __name__ == "__main__":
    unittest.main()
