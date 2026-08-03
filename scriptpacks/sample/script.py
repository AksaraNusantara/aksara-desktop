"""
===============================================================================

Aksara Nusantara

Module:
    scriptpacks.template.script

Module Type:
    ScriptPack Implementation

Purpose:
    Official ScriptPack template.

Implements:
    AN-STD-001

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


class SampleScriptPack(BaseScriptPack):
    """
    Official implementation of the Sample ScriptPack.
    """
    def get_characters(self):
        """
        Return all enabled Sample characters.
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

        TODO:
            Font registration will be implemented in AD-1.2.
        """
        pass

    def get_dataset_name(self) -> str:
        """
        Return the current dataset name.
        """

        return "sample"