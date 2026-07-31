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

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


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
    def get_characters(self) -> list[dict]:
        """
        Return the complete collection of characters provided
        by the ScriptPack.
        """
        raise NotImplementedError

    @abstractmethod
    def register_assets(self) -> None:
        """
        Register all runtime assets required by this ScriptPack.

        This method is invoked by the Core Engine after the
        ScriptPack has been successfully loaded and registered.

        Implementations may register fonts, preload images,
        initialize audio resources, or perform any other
        runtime asset initialization required before use.
        """
        raise NotImplementedError