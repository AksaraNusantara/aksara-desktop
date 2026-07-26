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

# None

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
    Official ScriptPack template.

    Copy this class when creating a new ScriptPack.
    """
    @property
    def identifier(self) -> str:
        return "sample"

    @property
    def name(self) -> str:
        return "Sample Template"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_characters(self):
        """
        Return ScriptPack character definitions.
        """
        raise NotImplementedError

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

