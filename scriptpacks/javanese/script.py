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
from PySide6.QtGui import QFontDatabase

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

    def register_assets(self) -> None:
        """
        Register runtime assets required by this ScriptPack.
        """
        #
        # Register every TrueType font bundled with this ScriptPack.
        #

        font_directory = (
            Path(__file__).parent
            / "assets"
            / "fonts"
        )

        if not font_directory.is_dir():
            raise FileNotFoundError(
                f"Font directory not found: {font_directory}"
            )

        #
        # Register every TrueType font bundled with this ScriptPack.
        #
        for font_file in sorted(font_directory.glob("*.ttf")):

            font_id = QFontDatabase.addApplicationFont(
                str(font_file)
            )

            if font_id == -1:
                raise RuntimeError(
                    f"Failed to register font: {font_file.name}"
                )

            families = QFontDatabase.applicationFontFamilies(
                    font_id
                )

            print(
                f"[ScriptPack] Registered font: "
                f"{font_file.name} -> {families}"
            )
