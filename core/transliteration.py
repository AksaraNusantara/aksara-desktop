"""
===============================================================================

Aksara Nusantara

Module:
    core.transliteration

Module Type:
    Core Contract

Purpose:
    Defines the script-independent Transliteration API types shared by the
    Core Engine and ScriptPacks: direction, diagnostics and result.

    This module SHALL NOT contain writing-system rules (TR-018). Concrete
    transliteration algorithms are owned by ScriptPacks.

Implements:
    AD-TR-01 TD-001 — Core Transliteration API as primary test boundary
    AD-TR-01 TD-002 — text, direction and script context
    AD-TR-01 TD-003 — output and diagnostics independent of the UI
    AN-STD-001 Section 17 — Transliteration

References:
    docs/development/transliteration/06. AD-TR-01 — Transliteration Contract Rules v0_1.md

    docs/development/transliteration/12. AD-TR-01 — Phase 2D-3 — Test Boundary & API Contract.md

    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

    docs/standards/PYTHON_MODULE_TEMPLATE.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: GPL-3.0-or-later

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

from dataclasses import dataclass
from enum import Enum

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

# None


class TransliterationDirection(str, Enum):
    """Direction of a transliteration operation (TR-001)."""

    LATIN_TO_SCRIPT = "latin_to_script"
    SCRIPT_TO_LATIN = "script_to_latin"


class DiagnosticCode(str, Enum):
    """
    Diagnostic categories defined by the transliteration contract (§22).
    """

    UNKNOWN = "unknown"
    """External character without a ScriptPack mapping. Preserved, not an error."""

    INVALID_CONTEXT = "invalid_context"
    """Known character used in an invalid context, e.g. a sandhangan without host."""

    UNSUPPORTED_SEQUENCE = "unsupported_sequence"
    """Sequence that cannot be formed or interpreted under the ScriptPack rules."""

    OPEN_CONTRACT = "open_contract"
    """Behaviour whose contract is still OPEN; the segment is preserved, not guessed."""


@dataclass(frozen=True)
class TransliterationDiagnostic:
    """
    A diagnostic attached to one segment of the input text.

    ``start`` and ``end`` are indices into the *input* text.
    """

    code: DiagnosticCode
    start: int
    end: int
    segment: str
    message: str
    rule: str = ""


@dataclass(frozen=True)
class TransliterationResult:
    """
    Result of a transliteration operation (TD-003).

    Segments that raise diagnostics other than ``UNKNOWN`` are preserved
    unchanged in ``output`` (partial processing principle, §23).
    """

    output: str
    direction: TransliterationDirection
    diagnostics: tuple[TransliterationDiagnostic, ...] = ()

    @property
    def is_complete(self) -> bool:
        """
        Return True when every segment was transliterated or deliberately
        preserved as an unknown external character.
        """

        return all(
            diagnostic.code is DiagnosticCode.UNKNOWN
            for diagnostic in self.diagnostics
        )
