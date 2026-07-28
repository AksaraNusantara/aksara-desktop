"""
===============================================================================

Aksara Nusantara

Module:
    scriptpacks.javanese.script

Module Type:
    ScriptPack Implementation

Purpose:
    Official implementation of the Javanese ScriptPack.

Implements:
    AN-STD-001

Writing System:
    Hanacaraka

Language:
    Javanese (jv)

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""

# =============================================================================
# Standard Library
# =============================================================================

from __future__ import annotations

import json
from pathlib import Path

# =============================================================================
# Local Project Imports
# =============================================================================

from core.scriptpack import BaseScriptPack


# -----------------------------------------------------------------------------
# Implements:
#
# AN-STD-001
# Official Javanese ScriptPack
# -----------------------------------------------------------------------------
class JavaneseScriptPack(BaseScriptPack):
    """
    Official implementation of the Javanese ScriptPack.
    """

    def get_characters(self) -> list[dict]:
        """
        Return all character definitions provided by
        the Javanese ScriptPack.
        """

        character_directory = (
            Path(__file__).parent
            / "assets"
            / "characters"
        )


        characters: list[dict] = []

        for json_file in sorted(character_directory.glob("*.json")):

            with json_file.open(
                "r",
                encoding="utf-8",
            ) as fp:

                repository = json.load(fp)

            if not isinstance(repository, list):
                raise ValueError(
                    f"{json_file.name} must contain a JSON array."
                )

            characters.extend(repository)

        return characters