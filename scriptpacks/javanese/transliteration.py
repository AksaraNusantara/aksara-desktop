"""
===============================================================================

Aksara Nusantara

Module:
    scriptpacks.javanese.transliteration

Module Type:
    ScriptPack Transliteration Engine

Purpose:
    Deterministic Latin <-> Aksara Jawa transliteration for the Javanese
    ScriptPack. Every glyph mapping is read from the ScriptPack character
    datasets in ``assets/characters``; this module only holds the grammar
    (tokenization, composition and decomposition).

    Only LOCKED contract rules are implemented. Behaviour that is still OPEN
    (e.g. ``ng`` before a consonant, TR-CR-001) is preserved unchanged and
    reported through a diagnostic instead of being guessed.

    The module is pure Python and does not depend on PySide6, UI state or
    persistence (TR-016, TR-017).

Implements:
    AD-TR-01 TR-001 through TR-018

Unicode notes:
    Text is produced and consumed in Unicode *logical* order:
    consonant, nukta, pasangan (pangkon + consonant), medial
    (cakra / pengkal / keret), vowel sign, final sign (cecak / layar /
    wignyan). Taling (U+A9BA) is therefore stored *after* its host even
    though the renderer draws it to the left; no codepoint reordering is
    performed. A taling that precedes its host (visual order) is reported
    as INVALID_CONTEXT.

References:
    docs/development/transliteration/06. AD-TR-01 — Transliteration Contract Rules v0_1.md

    tests/transliteration/contract_review/test_ng_cases.py

    docs/standards/PYTHON_MODULE_TEMPLATE.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.transliteration import DiagnosticCode
from core.transliteration import TransliterationDiagnostic
from core.transliteration import TransliterationDirection
from core.transliteration import TransliterationResult


INHERENT_VOWEL = "a"

_CONSONANT = "consonant"
_VOWEL = "vowel"

_ASCII_LOWER = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


@dataclass(frozen=True)
class _LatinToken:
    """A Latin letter token with its span in the input text."""

    kind: str
    value: str
    start: int
    end: int


class JavaneseTransliterator:
    """
    Data-driven Javanese transliteration engine.

    Instances are immutable after construction and safe to reuse.
    """

    def __init__(
        self,
        character_directory: Path,
    ) -> None:
        datasets = _load_datasets(character_directory)

        # ---------------------------------------------------------------
        # Forward tables (Latin -> Javanese)
        # ---------------------------------------------------------------

        self._base: dict[str, str] = {}

        for entry in datasets["nglegena"]:
            latin = entry["latin"]

            if latin.endswith(INHERENT_VOWEL):
                self._base[latin[: -len(INHERENT_VOWEL)]] = entry["glyph"]

        self._rekan: dict[str, str] = {
            entry["latin"]: entry["glyph"]
            for entry in datasets["rekan"]
        }

        self._onsets: dict[str, str] = {**self._base, **self._rekan}

        self._vowel_signs: dict[str, str] = {
            entry["latin"]: entry["glyph"]
            for entry in datasets["sandhangan_swara"]
        }

        self._swara: dict[str, str] = {
            entry["latin"]: entry["glyph"]
            for entry in datasets["swara"]
        }

        self._vowels: set[str] = (
            {INHERENT_VOWEL}
            | set(self._vowel_signs)
            | set(self._swara)
        )

        wyanjana = _by_id(datasets["sandhangan_wyanjana"])
        panyigeg = _by_id(datasets["sandhangan_panyigeg"])

        self._cakra = wyanjana["cakra"]
        self._pengkal = wyanjana["pengkal"]
        self._keret = wyanjana["keret"]
        self._pangkon = panyigeg["pangkon"]["glyph"]

        self._medials: dict[str, str] = {
            self._cakra["latin"]: self._cakra["glyph"],
            self._pengkal["latin"]: self._pengkal["glyph"],
        }

        self._codas: dict[str, str] = {
            panyigeg[identifier]["latin"]: panyigeg[identifier]["glyph"]
            for identifier in ("wignyan", "layar", "cecak")
        }

        self._cecak_latin = panyigeg["cecak"]["latin"]

        self._digits: dict[str, str] = {
            entry["latin"]: entry["glyph"]
            for entry in datasets["angka"]
        }

        self._punctuation: dict[str, str] = {
            entry["latin"]: entry["glyph"]
            for entry in datasets["pada"]
            if entry["latin"]
        }

        self._max_letter_token = max(
            len(token)
            for token in (*self._onsets, *self._vowels)
        )

        # ---------------------------------------------------------------
        # Reverse tables (Javanese -> Latin)
        # ---------------------------------------------------------------

        self._hosts: dict[str, tuple[str, str]] = {}

        for latin, glyph in self._base.items():
            self._hosts[glyph] = (latin, INHERENT_VOWEL)

        # Murda and Rekan follow the current ScriptPack data verbatim
        # (TR-009, TR-010): their ``latin`` value carries no inherent vowel.
        for entry in (*datasets["murda"], *datasets["rekan"]):
            self._hosts[entry["glyph"]] = (entry["latin"], "")

        self._max_host = max(len(glyph) for glyph in self._hosts)

        self._vowel_signs_reverse: dict[str, str] = {
            glyph: latin
            for latin, glyph in self._vowel_signs.items()
        }

        self._max_vowel_sign = max(
            len(glyph) for glyph in self._vowel_signs_reverse
        )

        self._medials_reverse: dict[str, str] = {
            glyph: latin
            for latin, glyph in self._medials.items()
        }

        self._codas_reverse: dict[str, str] = {
            glyph: latin
            for latin, glyph in self._codas.items()
        }

        self._swara_reverse = _invert(self._swara)
        self._digits_reverse = _invert(self._digits)
        self._punctuation_reverse = _invert(self._punctuation)

        self._open_punctuation: set[str] = {
            entry["glyph"]
            for entry in datasets["pada"]
            if not entry["latin"]
        }

        self._dependent_marks: set[str] = set()

        for glyph in (
            *self._vowel_signs.values(),
            *self._medials.values(),
            *self._codas.values(),
            self._keret["glyph"],
            self._pangkon,
        ):
            self._dependent_marks.update(glyph)

        for glyph in self._rekan.values():
            self._dependent_marks.update(glyph[1:])

        self._taling = self._vowel_signs["e"]

    # =====================================================================
    # Public API
    # =====================================================================

    def transliterate(
        self,
        text: str,
        direction: TransliterationDirection,
    ) -> TransliterationResult:
        """Transliterate ``text`` in the given direction."""

        direction = TransliterationDirection(direction)

        if direction is TransliterationDirection.LATIN_TO_SCRIPT:
            output, diagnostics = self._latin_to_javanese(text)
        else:
            output, diagnostics = self._javanese_to_latin(text)

        return TransliterationResult(
            output=output,
            direction=direction,
            diagnostics=tuple(diagnostics),
        )

    # =====================================================================
    # Latin -> Javanese
    # =====================================================================

    def _latin_to_javanese(
        self,
        text: str,
    ) -> tuple[str, list[TransliterationDiagnostic]]:
        folded = text.translate(_ASCII_LOWER)
        out: list[str] = []
        diagnostics: list[TransliterationDiagnostic] = []
        word: list[_LatinToken] = []

        i = 0

        while i < len(text):
            token = self._match_letter(folded, i)

            if token is not None:
                word.append(token)
                i = token.end
                continue

            if word:
                self._compose_word(text, word, out, diagnostics)
                word = []

            character = text[i]

            if character in self._digits:
                out.append(self._digits[character])
            elif character in self._punctuation:
                out.append(self._punctuation[character])
            else:
                self._preserve_unknown(text, i, out, diagnostics)

            i += 1

        if word:
            self._compose_word(text, word, out, diagnostics)

        return "".join(out), diagnostics

    def _match_letter(
        self,
        folded: str,
        index: int,
    ) -> _LatinToken | None:
        """Longest valid Latin letter token at ``index`` (§20.3)."""

        for length in range(self._max_letter_token, 0, -1):
            candidate = folded[index : index + length]

            if len(candidate) != length:
                continue

            if candidate in self._onsets:
                kind = _CONSONANT
            elif candidate in self._vowels:
                kind = _VOWEL
            else:
                continue

            return _LatinToken(kind, candidate, index, index + length)

        return None

    def _compose_word(
        self,
        text: str,
        word: list[_LatinToken],
        out: list[str],
        diagnostics: list[TransliterationDiagnostic],
    ) -> None:
        """Compose one run of Latin letter tokens into Javanese."""

        i = 0
        n = len(word)

        while i < n:
            token = word[i]

            # -- Independent vowel (TR-008) --------------------------------
            if token.kind == _VOWEL:
                glyph = self._swara.get(token.value)

                if glyph is None:
                    self._preserve(
                        text, word[i:i + 1], out, diagnostics,
                        DiagnosticCode.UNSUPPORTED_SEQUENCE,
                        f"No swara is defined for vowel '{token.value}'.",
                        "TR-008",
                    )
                    i += 1
                    continue

                out.append(glyph)
                i = self._compose_coda(text, word, i + 1, out, diagnostics)
                continue

            # -- Consonant with vowel (TR-002, TR-003, TR-004) -------------
            syllable = self._syllable_nucleus(word, i)

            if syllable is not None:
                medial, vowel_index = syllable
                out.append(
                    self._syllable_glyphs(
                        token.value,
                        medial,
                        word[vowel_index].value,
                    )
                )
                i = self._compose_coda(
                    text, word, vowel_index + 1, out, diagnostics,
                )
                continue

            # -- Consonant without vowel -----------------------------------
            if token.value == self._cecak_latin:
                self._preserve(
                    text, word[i:i + 1], out, diagnostics,
                    DiagnosticCode.OPEN_CONTRACT,
                    "Resolution of 'ng' without a preceding vowel or before "
                    "a consonant is OPEN (nglegena vs. panyigeg).",
                    "TR-CR-001",
                )
                i += 1
                continue

            if i + 1 == n:
                # Word-final dead consonant: pangkon (TR-006). Rekan tokens
                # map to the bare rekan glyph (TR-009 golden cases).
                glyph = self._onsets[token.value]

                if token.value not in self._rekan:
                    glyph += self._pangkon

                out.append(glyph)
                i += 1
                continue

            if self._syllable_nucleus(word, i + 1) is None:
                # More than one dead consonant in a row, or a cakra/pengkal
                # cluster without a vowel (e.g. 'kry', §22).
                end = i

                while end + 1 < n and word[end + 1].kind == _CONSONANT:
                    end += 1

                if end + 1 < n:
                    end += 1

                self._preserve(
                    text, word[i:end + 1], out, diagnostics,
                    DiagnosticCode.UNSUPPORTED_SEQUENCE,
                    "Consonant sequence cannot be formed with a single "
                    "pasangan or sandhangan wyanjana.",
                    "TR-007",
                )
                i = end + 1
                continue

            # Dead consonant followed by a syllable: pasangan (TR-007).
            # Unicode encodes pasangan as pangkon + following consonant.
            out.append(self._onsets[token.value] + self._pangkon)
            i += 1

    def _syllable_nucleus(
        self,
        word: list[_LatinToken],
        index: int,
    ) -> tuple[str | None, int] | None:
        """
        Return ``(medial, vowel_index)`` when the consonant at ``index``
        carries a vowel, directly or through cakra / pengkal.
        """

        n = len(word)

        if index + 1 < n and word[index + 1].kind == _VOWEL:
            return None, index + 1

        if (
            index + 2 < n
            and word[index + 1].kind == _CONSONANT
            and word[index + 1].value in self._medials
            and word[index + 2].kind == _VOWEL
        ):
            return word[index + 1].value, index + 2

        return None

    def _syllable_glyphs(
        self,
        consonant: str,
        medial: str | None,
        vowel: str,
    ) -> str:
        """Build host + medial + vowel sign in Unicode logical order."""

        glyphs = self._onsets[consonant]

        if medial == self._cakra["latin"] and medial + vowel == self._keret["latin"]:
            # Keret = cakra + pepet in a single sign (TR-004).
            return glyphs + self._keret["glyph"]

        if medial is not None:
            glyphs += self._medials[medial]

        if vowel != INHERENT_VOWEL:
            glyphs += self._vowel_signs[vowel]

        return glyphs

    def _compose_coda(
        self,
        text: str,
        word: list[_LatinToken],
        index: int,
        out: list[str],
        diagnostics: list[TransliterationDiagnostic],
    ) -> int:
        """Apply sandhangan panyigeg after a vowel (TR-005)."""

        n = len(word)

        if (
            index >= n
            or word[index].kind != _CONSONANT
            or word[index].value not in self._codas
        ):
            return index

        value = word[index].value
        following = word[index + 1] if index + 1 < n else None

        if following is not None and following.kind == _VOWEL:
            # The consonant starts the next syllable instead.
            return index

        if value == self._cecak_latin and following is not None:
            self._preserve(
                text, word[index:index + 1], out, diagnostics,
                DiagnosticCode.OPEN_CONTRACT,
                "Resolution of 'ng' before a consonant is OPEN "
                "(cecak vs. nglegena + pasangan).",
                "TR-CR-001",
            )
            return index + 1

        out.append(self._codas[value])
        return index + 1

    # =====================================================================
    # Javanese -> Latin
    # =====================================================================

    def _javanese_to_latin(
        self,
        text: str,
    ) -> tuple[str, list[TransliterationDiagnostic]]:
        out: list[str] = []
        diagnostics: list[TransliterationDiagnostic] = []

        n = len(text)
        i = 0

        while i < n:
            host = _longest_match(text, i, self._hosts, self._max_host)

            if host is not None:
                i = self._decompose_syllable(text, i, host, out)
                continue

            character = text[i]

            if character in self._swara_reverse:
                out.append(self._swara_reverse[character])
                i = self._decompose_coda(text, i + 1, out)
                continue

            if character in self._digits_reverse:
                out.append(self._digits_reverse[character])
            elif character in self._punctuation_reverse:
                out.append(self._punctuation_reverse[character])
            elif character in self._open_punctuation:
                out.append(character)
                diagnostics.append(
                    TransliterationDiagnostic(
                        code=DiagnosticCode.OPEN_CONTRACT,
                        start=i,
                        end=i + 1,
                        segment=character,
                        message="Latin mapping for this pada is OPEN.",
                        rule="AD-TR-01 §27",
                    )
                )
            elif character in self._dependent_marks:
                message = "Sandhangan or modifier has no host consonant."

                if character == self._taling:
                    message += (
                        " Taling must follow its host in Unicode logical "
                        "order; the renderer displays it to the left."
                    )

                out.append(character)
                diagnostics.append(
                    TransliterationDiagnostic(
                        code=DiagnosticCode.INVALID_CONTEXT,
                        start=i,
                        end=i + 1,
                        segment=character,
                        message=message,
                        rule="AD-TR-01 §22",
                    )
                )
            else:
                self._preserve_unknown(text, i, out, diagnostics)

            i += 1

        return "".join(out), diagnostics

    def _decompose_syllable(
        self,
        text: str,
        index: int,
        host: str,
        out: list[str],
    ) -> int:
        """Decompose host [medial] [vowel sign | pangkon] [panyigeg]."""

        consonant, inherent = self._hosts[host]
        j = index + len(host)
        n = len(text)

        if j < n and text[j] == self._keret["glyph"]:
            out.append(consonant + self._keret["latin"])
            return self._decompose_coda(text, j + 1, out)

        medial = ""

        if j < n and text[j] in self._medials_reverse:
            medial = self._medials_reverse[text[j]]
            j += 1

        vowel_sign = _longest_match(
            text, j, self._vowel_signs_reverse, self._max_vowel_sign,
        )

        if vowel_sign is not None:
            out.append(consonant + medial + self._vowel_signs_reverse[vowel_sign])
            return self._decompose_coda(text, j + len(vowel_sign), out)

        if j < n and text[j] == self._pangkon:
            # Pangkon, or the first half of a pasangan when a consonant
            # follows; both remove the inherent vowel (TR-006, TR-007).
            out.append(consonant + medial)
            return j + 1

        out.append(consonant + medial + inherent)
        return self._decompose_coda(text, j, out)

    def _decompose_coda(
        self,
        text: str,
        index: int,
        out: list[str],
    ) -> int:
        if index < len(text) and text[index] in self._codas_reverse:
            out.append(self._codas_reverse[text[index]])
            return index + 1

        return index

    # =====================================================================
    # Shared helpers
    # =====================================================================

    @staticmethod
    def _preserve(
        text: str,
        tokens: list[_LatinToken],
        out: list[str],
        diagnostics: list[TransliterationDiagnostic],
        code: DiagnosticCode,
        message: str,
        rule: str,
    ) -> None:
        """Preserve a Latin segment unchanged and record a diagnostic."""

        start = tokens[0].start
        end = tokens[-1].end
        segment = text[start:end]

        out.append(segment)
        diagnostics.append(
            TransliterationDiagnostic(
                code=code,
                start=start,
                end=end,
                segment=segment,
                message=message,
                rule=rule,
            )
        )

    @staticmethod
    def _preserve_unknown(
        text: str,
        index: int,
        out: list[str],
        diagnostics: list[TransliterationDiagnostic],
    ) -> None:
        """Preserve an unmapped character (TR-012, TR-013, TR-014)."""

        character = text[index]
        out.append(character)

        if not character.isspace():
            diagnostics.append(
                TransliterationDiagnostic(
                    code=DiagnosticCode.UNKNOWN,
                    start=index,
                    end=index + 1,
                    segment=character,
                    message="Character has no ScriptPack mapping; preserved.",
                    rule="TR-014",
                )
            )


_DATASETS = (
    "angka",
    "murda",
    "nglegena",
    "pada",
    "rekan",
    "sandhangan_panyigeg",
    "sandhangan_swara",
    "sandhangan_wyanjana",
    "swara",
)


def _load_datasets(
    character_directory: Path,
) -> dict[str, list[dict]]:
    datasets: dict[str, list[dict]] = {}

    for name in _DATASETS:
        path = Path(character_directory) / f"{name}.json"

        with path.open("r", encoding="utf-8") as fp:
            datasets[name] = json.load(fp)

    return datasets


def _by_id(
    entries: list[dict],
) -> dict[str, dict]:
    return {entry["id"]: entry for entry in entries}


def _invert(
    mapping: dict[str, str],
) -> dict[str, str]:
    return {glyph: latin for latin, glyph in mapping.items()}


def _longest_match(
    text: str,
    index: int,
    table: dict[str, object],
    max_length: int,
) -> str | None:
    for length in range(max_length, 0, -1):
        candidate = text[index : index + length]

        if len(candidate) == length and candidate in table:
            return candidate

    return None
