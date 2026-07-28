"""
===============================================================================

Aksara Nusantara

Module:
    core.template.script

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


class TemplateScriptPack(BaseScriptPack):
    """
    Official ScriptPack template.

    Copy this class when creating a new ScriptPack.
    """
    def get_characters(self):
        """
        Return ScriptPack character definitions.
        """
        raise NotImplementedError
