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

from pathlib import Path
import json

# =============================================================================
# Third-party Packages
# =============================================================================

# None

# =============================================================================
# Local Project Imports
# =============================================================================

from core.scriptpack import BaseScriptPack


class JavaneseScriptPack(BaseScriptPack):
    """
    Official Javanese ScriptPack.
    """
    @property
    def identifier(self) -> str:
        return "javanese"

    @property
    def name(self) -> str:
        return "Javanese Script"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_characters(self) -> list[dict]:
        """
        Return all enabled Javanese characters.
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
                encoding="utf-8"
            ) as fp:

                data = json.load(fp)

            characters.extend(data["characters"])

        return characters

    def transliterate(
        self,
        text: str,
    ) -> str:
        """
        Transliterate text.

        This method SHALL be implemented by
        concrete ScriptPacks.
        """
        raise NotImplementedError

    def get_audio(
        self,
        identifier: str,
    ):
        """
        Return audio resource.

        Reserved for future implementation.
        """
        raise NotImplementedError

