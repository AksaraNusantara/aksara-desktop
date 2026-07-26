"""
===============================================================================

Aksara Nusantara

Module:
    core.scriptpack

Purpose:
    Defines the abstract base interface for all ScriptPack implementations.

Implements:
    AN-STD-001
    Section 11 - BaseScriptPack Interface

References:
    docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md
    docs/development/TRACEABILITY.md

Copyright (c) Aksara Nusantara Project

SPDX-License-Identifier: MIT

===============================================================================
"""
from abc import ABC, abstractmethod


# -----------------------------------------------------------------------------
# Implements:
#
# AN-STD-001
# Section 11
# BaseScriptPack Interface
# -----------------------------------------------------------------------------
class BaseScriptPack(ABC):
    """
    Abstract base class for all ScriptPack implementations.

    Every ScriptPack SHALL inherit from this class and implement
    the required interface defined by the ScriptPack Specification.

    This class defines the minimum contract required by the
    Aksara Nusantara Core Engine.
    """
    
    @abstractmethod
    def get_characters(self):
        """
        Return the complete collection of characters provided by the ScriptPack.
        """
        pass
